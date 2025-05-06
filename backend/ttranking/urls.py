from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler404, handler500
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/', include('core.urls')),
    path('api/players/', include('players.urls')),
    path('api/matches/', include('matches.urls')),
    path('api/seasons/', include('seasons.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
