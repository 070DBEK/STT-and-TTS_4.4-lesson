#!/usr/bin/env python
"""
Script to create a superuser
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User


def main():
    """Create superuser if it doesn't exist"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully!")
        print(f"Email: {email}")
        print(f"Password: {password}")
    else:
        print(f"Superuser '{username}' already exists!")


if __name__ == '__main__':
    main()
