#!/usr/bin/env python
"""
Script to set up the database with all migrations
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from django.core.management import execute_from_command_line

def main():
    """Create and apply migrations for all apps"""
    print("Creating migrations for users app...")
    execute_from_command_line(['manage.py', 'makemigrations', 'users'])

    print("Creating migrations for stt app...")
    execute_from_command_line(['manage.py', 'makemigrations', 'stt'])

    print("Creating migrations for tts app...")
    execute_from_command_line(['manage.py', 'makemigrations', 'tts'])

    print("Applying all migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

    print("Database setup completed successfully!")


if __name__ == '__main__':
    main()
