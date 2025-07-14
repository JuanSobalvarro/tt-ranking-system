from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from core.models import SoftDeleteModel
from profiles.enums import Handedness, PlayStyle, GripType, Dominance, SexChoices, CountryChoices
import os
import io
from uuid import uuid4
from PIL import Image, UnidentifiedImageError
from datetime import date


DESIRED_IMG_SIZE = (600, 600)
UPLOAD_DIR = 'avatars/'

def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError(_("Image file too large (max 5 MB)."))

def get_avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    return os.path.join(UPLOAD_DIR, f'{uuid4().hex}.{ext}')


class UserProfile(AbstractUser, SoftDeleteModel):
    """
    Custom user model.
    """
    birth_date = models.DateField(null=True, blank=True, default=None)
    sex = models.CharField(max_length=6, choices=SexChoices.choices,  null=True, blank=True, default=SexChoices.MALE)
    nationality = models.CharField(max_length=50, choices=CountryChoices.choices, null=True, blank=True, default=CountryChoices.NI)

    # Roles and permissions (for easy access control)
    is_player = models.BooleanField(default=False)
    is_referee = models.BooleanField(default=False)

    # Image and description (shared visual profile fields)
    image = models.ImageField(upload_to=get_avatar_upload_path, validators=[validate_image_size], null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True)

    @property
    def age(self) -> int:
        if not self.birth_date:
            return None
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def __str__(self):
        return self.username

    def has_role(self, role):
        if role == 'player':
            return self.is_player
        elif role == 'referee':
            return self.is_referee
        return False

    def get_role_display(self):
        if self.is_superuser:
            return "Admin"
        elif self.is_referee:
            return "Referee"
        elif self.is_player:
            return "Player"
        return "User"

    def resize_and_crop(self, img, size):
        img.thumbnail(size, Image.Resampling.LANCZOS)
        return img

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = UserProfile.objects.filter(pk=self.pk).first()
            old_photo = old_instance.image if old_instance else None
        else:
            old_photo = None

        if self.image and (not old_photo or old_photo != self.image):
            # Delete old photo
            if old_photo and old_photo.path and os.path.exists(old_photo.path):
                try:
                    os.remove(old_photo.path)
                except Exception:
                    pass  # or log the failure

            # Get file extension and new path
            ext = self.image.name.split('.')[-1].lower()
            valid_exts = ['png', 'jpg', 'jpeg', 'webp']
            ext = ext if ext in valid_exts else 'png'  # fallback to png
            file_path = os.path.join(UPLOAD_DIR, f'{uuid4().hex}.{ext}')

            # Open image
            try:
                image = Image.open(self.image)
            except UnidentifiedImageError:
                raise ValidationError(_("Uploaded file is not a valid image."))

            # Ensure RGBA or RGB based on format
            if ext == 'png' or image.mode == 'RGBA':
                image = image.convert('RGBA')  # preserve transparency
            else:
                image = image.convert('RGB')  # remove alpha for jpg

            # Resize
            image = self.resize_and_crop(image, DESIRED_IMG_SIZE)

            # Save to memory
            buffer = io.BytesIO()
            image.save(buffer, format=ext.upper())
            buffer.seek(0)

            # Assign to ImageField
            self.image.save(file_path, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)


class PlayerProfile(SoftDeleteModel):
    """
    Player-specific profile.
    """
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='player_profile')

    alias = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    is_premium = models.BooleanField(default=False)
    handedness = models.CharField(max_length=12, choices=Handedness.choices, default=Handedness.RIGHT)
    play_style = models.CharField(max_length=20, choices=PlayStyle.choices, default=PlayStyle.ALL_ROUNDER)
    grip_type = models.CharField(max_length=10, choices=GripType.choices, default=GripType.FREE)
    dominance = models.CharField(max_length=10, choices=Dominance.choices, default=Dominance.BOTH)

    @property
    def matches_played(self):
        # reverse relation for rankings (which have a foreign key to PlayerProfile)

        # if not self.rankings:
        #     return 0

        rankings = self.rankings.all()

        count = 0
        for ranking in rankings:
            count += ranking.matches_played

        return count

    def __str__(self):
        return f"{self.alias} ({self.profile.username})"


class RefereeProfile(SoftDeleteModel):
    """
    Referee-specific profile.
    """
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='referee_profile')

    alias = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    identifier = models.CharField(max_length=30, unique=True)

    matches_refereed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.alias or self.profile.username} - Referee"

