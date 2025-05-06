from django import forms
from django.core.exceptions import ValidationError
from django.utils.dateformat import format
from django.utils.translation import gettext_lazy as _
from .models import Player, COUNTRY_CHOICES, GENDER_CHOICES
import imghdr
import datetime

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'alias', 'gender', 'date_of_birth', 'nationality', 'ranking', 'photo']
        labels = {
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'alias': _('Apodo'),
            'gender': _('Sexo'),
            'date_of_birth': _('Fecha de nacimiento'),
            'nationality': _('Nacionalidad'),
            'ranking': _('Ranking'),
            'photo': _('Foto'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'alias': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'gender': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}, choices=GENDER_CHOICES),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'type': 'date'}, format='%Y-%m-%d'),
            'nationality': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}, choices=COUNTRY_CHOICES),
            'ranking': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'Initial Ranking Points'}),
            'photo': forms.FileInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.date_of_birth:
                self.fields['date_of_birth'].initial = self.instance.date_of_birth.strftime('%Y-%m-%d')
            self.fields['gender'].initial = self.instance.gender

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            image_type = imghdr.what(photo)
            if image_type not in ['jpeg', 'png']:
                raise ValidationError("Unsupported file type. Please upload a JPEG or PNG image.")
        return photo