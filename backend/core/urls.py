# ttranking/core/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.APIRootView.as_view(), name='api_root'),
    path('token/', TokenObtainPairView.as_view(), name='api_token'),
    path('token-refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('admin/home/', views.AdminHomeView.as_view(), name='admin_home')
]
