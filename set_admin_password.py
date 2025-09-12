#!/usr/bin/env python3
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get admin user and set password
admin_user = User.objects.get(username='admin')
admin_user.set_password('admin123')
admin_user.is_email_verified = True  # Mark email as verified for admin
admin_user.save()

print("Admin password set to 'admin123' and email verified!")