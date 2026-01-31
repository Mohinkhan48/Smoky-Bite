import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

def update_specials():
    # 1. Define the exact data from the image
    specials_data = {
        'HOT & SPICY': [
            ('LEG PIECE ( 1 PCS )', 70),
            ('LOLLIPOP ( 4 PCS )', 120),
            ('WINGS ( 5 PCS )', 130),
            ('TIKKA ( 8 PCS )', 140),
        ],
        'PERI PERI': [
            ('LEG PIECE ( 1 PCS )', 80),
            ('LOLLIPOP ( 4 PCS )', 130),
            ('WINGS ( 5 PCS )', 140),
            ('TIKKA ( 8 PCS )', 150),
        ],
        'MALAI SPECIAL': [
            ('LEG PIECE ( 1 PCS )', 90),
            ('LOLLIPOP ( 4 PCS )', 140),
            ('WINGS ( 5 PCS )', 150),
            ('TIKKA ( 8 PCS )', 160),
        ]
    }

    # Combos are a bit different, we'll treat them as single items for ordering
    # but we'll need to handle the display of their contents in the template
    combos_data = {
        'MEDIUM COMBO': 399,
        'LARGE COMBO': 599
    }

    print("Updating Specials Menu...")

    # 2. Update Standard 3 Categories
    for cat_name, items in specials_data.items():
        # Get or Create Category
        category, created = Category.objects.get_or_create(name=cat_name)
        print(f"Category: {cat_name}")
        
        # Clear existing items in this category to ensure exact match
        category.items.all().delete()
        
        for item_name, price in items:
            MenuItem.objects.create(category=category, name=item_name, price=price)
            print(f"  - Added: {item_name} @ {price}")

    # 3. Handle Combos
    # We'll create a category "COMBOS" to hold them
    combo_cat, _ = Category.objects.get_or_create(name="COMBOS")
    combo_cat.items.all().delete()
    print("Category: COMBOS")
    
    MenuItem.objects.create(category=combo_cat, name="MEDIUM COMBO", price=399)
    print("  - Added: MEDIUM COMBO @ 399")
    
    MenuItem.objects.create(category=combo_cat, name="LARGE COMBO", price=599)
    print("  - Added: LARGE COMBO @ 599")

    print("Specials update complete.")

if __name__ == '__main__':
    update_specials()
