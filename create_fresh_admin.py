import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from django.contrib.auth.models import User

def create_fresh_admin():
    username = 'admin_smoky'
    password = 'admin123'
    
    # Delete if already exists to ensure fresh start
    User.objects.filter(username=username).delete()
    
    User.objects.create_superuser(username, 'admin@example.com', password)
    print(f"SUCCESS: Created fresh superuser '{username}' with password '{password}'")

if __name__ == "__main__":
    create_fresh_admin()
