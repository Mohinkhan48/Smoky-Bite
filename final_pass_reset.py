import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from django.contrib.auth.models import User

def reset():
    print("--- STARTING RESET ---")
    users = User.objects.all()
    print(f"Found {len(users)} users.")
    for u in users:
        print(f"Checking: '{u.username}'")
        
    target = 'Smokybites'
    u, created = User.objects.get_or_create(username=target)
    
    u.set_password('admin123')
    u.is_superuser = True
    u.is_staff = True
    u.is_active = True
    u.save()
    
    print(f"SUCCESS: User '{target}' password set to 'admin123'")
    print(f"User Active: {u.is_active}")
    print(f"User Staff: {u.is_staff}")
    print(f"User Superuser: {u.is_superuser}")
    print("--- RESET COMPLETE ---")

if __name__ == "__main__":
    reset()
