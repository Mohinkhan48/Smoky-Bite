import os
import django
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import MenuItem

def check_items():
    print("Checking for duplicate MenuItems...")
    duplicates = MenuItem.objects.values('category', 'name').annotate(count=Count('id')).filter(count__gt=1)
    
    if not duplicates:
        print("No duplicate items found.")
    else:
        for entry in duplicates:
             print(f"Found {entry['count']} copies of '{entry['name']}' in category {entry['category']}")

if __name__ == "__main__":
    check_items()
