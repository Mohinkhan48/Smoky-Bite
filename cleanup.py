import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

def cleanup_duplicates():
    print("Checking for duplicates...")
    specials_names = ['HOT & SPICY', 'PERI PERI', 'MALAI SPECIAL', 'COMBOS']
    
    for name in specials_names:
        # Find all categories with this name (in case multiple categories were created)
        cats = Category.objects.filter(name=name)
        print(f"Category '{name}': Found {cats.count()} instances")
        
        # If we have multiple categories of the same name, or even just one with many items
        if cats.exists():
            # Delete ALL of them and their items to start fresh
            count = cats.count()
            cats.delete() 
            print(f"  Deleted {count} categories (and their items).")

    print("Re-populating Specials freshly...")
    
    specials_data = {
        'HOT & SPICY': [('LEG PIECE ( 1 PCS )', 70), ('LOLLIPOP ( 4 PCS )', 120), ('WINGS ( 5 PCS )', 130), ('TIKKA ( 8 PCS )', 140)],
        'PERI PERI': [('LEG PIECE ( 1 PCS )', 80), ('LOLLIPOP ( 4 PCS )', 130), ('WINGS ( 5 PCS )', 140), ('TIKKA ( 8 PCS )', 150)],
        'MALAI SPECIAL': [('LEG PIECE ( 1 PCS )', 90), ('LOLLIPOP ( 4 PCS )', 140), ('WINGS ( 5 PCS )', 150), ('TIKKA ( 8 PCS )', 160)]
    }
    
    for cat_name, items in specials_data.items():
        cat = Category.objects.create(name=cat_name)
        for name, price in items:
            MenuItem.objects.create(category=cat, name=name, price=price)
        print(f"  Created '{cat_name}' with {len(items)} items")

    # Combos
    combo_cat = Category.objects.create(name="COMBOS")
    MenuItem.objects.create(category=combo_cat, name="MEDIUM COMBO", price=399)
    MenuItem.objects.create(category=combo_cat, name="LARGE COMBO", price=599)
    print("  Created 'COMBOS' with 2 items")

if __name__ == "__main__":
    cleanup_duplicates()
