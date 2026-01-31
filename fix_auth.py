import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from django.contrib.auth.models import User

print("--- AUTH DIAGNOSTICS ---")
users = User.objects.all()
if not users:
    print("NO USERS FOUND IN DATABASE.")
else:
    for u in users:
        print(f"Username: '{u.username}' | Staff: {u.is_staff} | Superuser: {u.is_superuser}")

# Ensure at least one superuser exists with a known password if requested
# Let's check for 'Smokybites' specifically
target_user = "Smokybites"
if not User.objects.filter(username=target_user).exists():
    print(f"\nCreating superuser '{target_user}'...")
    User.objects.create_superuser(target_user, 'admin@example.com', 'admin123')
    print("User created: Username 'Smokybites', Password 'admin123'")
else:
    u = User.objects.get(username=target_user)
    u.set_password('admin123')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f"\nPassword for existing user '{target_user}' reset to 'admin123'")

print("\n--- DONE ---")
