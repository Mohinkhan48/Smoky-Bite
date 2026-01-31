import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from django.contrib.auth.models import User

def list_users():
    users = User.objects.all()
    print("--- USER LIST ---")
    for u in users:
        print(f"Username: '{u.username}' | Superuser: {u.is_superuser} | Staff: {u.is_staff} | Active: {u.is_active}")
    print("-----------------")

if __name__ == "__main__":
    list_users()
