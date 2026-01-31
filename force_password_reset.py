import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from django.contrib.auth.models import User

def reset_password():
    username = 'Smokybites'
    new_password = 'admin123'
    
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"SUCCESS: Password for '{username}' has been reset to '{new_password}'.")
        print("You can now log in and change it to your desired password.")
    except User.DoesNotExist:
        # Create it if it doesn't exist
        User.objects.create_superuser(username, 'admin@example.com', new_password)
        print(f"SUCCESS: Superuser '{username}' created with password '{new_password}'.")

if __name__ == "__main__":
    reset_password()
