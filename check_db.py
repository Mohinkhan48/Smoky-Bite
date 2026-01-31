
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

print(f"Categories count: {Category.objects.count()}")
print(f"Items count: {MenuItem.objects.count()}")

for c in Category.objects.all():
    print(f"Category: {c.name} (Active: {c.is_active})")
    print(f"  Items: {c.items.count()}")
