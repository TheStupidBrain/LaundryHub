import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laundry_project.settings')
django.setup()

from core.models import User
from django.contrib.auth.hashers import make_password

try:
    user = User.objects.filter(email='admin@store.com').first()
    if user:
        user.set_password('admin123')
        user.save()
        print("Updated password for existing user")
    else:
        User.objects.create(
            name='Super Admin',
            email='admin@store.com',
            phone='0000000000',
            password=make_password('admin123'),
            user_type='Admin'
        )
        print("Created new user")
except Exception as e:
    print(f"Error: {e}")
