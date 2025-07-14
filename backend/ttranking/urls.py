from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler404, handler500
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/core/', include('core.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/admin/', admin.site.urls),
    path('seasons/', include('seasons.urls')),
    # path('players/', include('players.urls')),
    # path('matches/', include('matches.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
