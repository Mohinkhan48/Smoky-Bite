import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category

print("Checking Categories and Items:")
for c in Category.objects.all():
    print(f"Category: {c.name} - Items: {c.items.count()}")
    for i in c.items.all()[:3]:
        print(f" - {i.name}: {i.price}")
