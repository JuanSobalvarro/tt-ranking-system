from django.contrib import admin
from .models import UserProfile, PlayerProfile, RefereeProfile

admin.site.register(UserProfile)
admin.site.register(PlayerProfile)
admin.site.register(RefereeProfile)
