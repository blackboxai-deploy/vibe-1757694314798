"""
URLs for accounts app
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    
    # Profile and settings URLs
    path('profile/', views.profile_view, name='profile'),
    
    # Ajax URLs
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    
    # Dashboard URL (main landing page after login)
    path('dashboard/', views.dashboard_view, name='dashboard'),
]