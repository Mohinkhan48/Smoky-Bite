
import os
import django
import sys

# Redirect stdout/stderr to file
sys.stdout = open('debug_output.txt', 'w')
sys.stderr = sys.stdout

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
    django.setup()

    from orders.models import Category, MenuItem

    cat_count = Category.objects.count()
    item_count = MenuItem.objects.count()

    print(f"Categories: {cat_count}")
    print(f"Items: {item_count}")

    if cat_count == 0:
        print("Database is empty! Attempting simpler populate...")
        # Emergency populate
        c = Category.objects.create(name="TEST CATEGORY")
        MenuItem.objects.create(category=c, name="TEST ITEM", price=100)
        print("Created test data.")
    else:
        for c in Category.objects.all():
            print(f"- {c.name}: {c.items.count()} items")

except Exception as e:
    print(f"ERROR: {e}")
