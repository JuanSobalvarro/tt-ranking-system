from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import date
from PIL import Image
from io import BytesIO

from profiles.models import UserProfile, PlayerProfile, RefereeProfile


def generate_test_image(name="test.png", size=(1000, 1000), color="blue"):
    image = Image.new("RGB", size, color=color)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/png")


class UserProfileModelTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            birth_date=date(2000, 1, 1)
        )

    def test_age_property(self):
        expected_age = date.today().year - 2000
        if (date.today().month, date.today().day) < (1, 1):
            expected_age -= 1
        self.assertEqual(self.user.age, expected_age)

    def test_role_display_player(self):
        self.user.is_player = True
        self.user.save()
        self.assertEqual(self.user.get_role_display(), "Player")

    def test_role_display_referee(self):
        self.user.is_referee = True
        self.user.save()
        self.assertEqual(self.user.get_role_display(), "Referee")

    def test_avatar_resizing_on_save(self):
        image_file = generate_test_image()
        self.user.image = image_file
        self.user.save()
        self.assertTrue(self.user.image.width <= 600 and self.user.image.height <= 600)


class PlayerProfileModelTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user(username="player", password="pass")
        self.player = PlayerProfile.objects.create(profile=self.user, alias="pingponghero")

    def test_player_flag_set_on_save(self):
        self.player.refresh_from_db()
        self.assertTrue(self.player.profile.is_player)

    def test_matches_played_property_defaults_to_zero(self):
        self.assertEqual(self.player.matches_played, 0)


class RefereeProfileModelTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user(username="referee", password="pass")
        self.referee = RefereeProfile.objects.create(profile=self.user, alias="ref001", identifier="ref001")

    def test_referee_flag_set_on_save(self):
        self.referee.refresh_from_db()
        self.assertTrue(self.referee.profile.is_referee)

    def test_str_representation(self):
        self.assertIn("ref001", str(self.referee))
