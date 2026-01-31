import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category

print("Existing Categories:")
for c in Category.objects.all():
    print(f"'{c.name}'")
