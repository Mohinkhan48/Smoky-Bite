import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

def reset_specials():
    target_categories = ['HOT & SPICY', 'PERI PERI', 'MALAI SPECIAL', 'COMBOS']
    
    print("--- Resetting Specials Page ---")
    
    # 1. DELETE existing categories completely to remove duplicates
    for name in target_categories:
        cats = Category.objects.filter(name=name)
        count = cats.count()
        if count > 0:
            print(f"Deleting {count} existing '{name}' categories...")
            cats.delete()
            
    print("Existing specials cleared.")
    
    # 2. Re-create exactly as per image
    specials_data = {
        'HOT & SPICY': [
            ('LEG PIECE ( 1 PCS )', 70), 
            ('LOLLIPOP ( 4 PCS )', 120), 
            ('WINGS ( 5 PCS )', 130), 
            ('TIKKA ( 8 PCS )', 140)
        ],
        'PERI PERI': [
            ('LEG PIECE ( 1 PCS )', 80), 
            ('LOLLIPOP ( 4 PCS )', 130), 
            ('WINGS ( 5 PCS )', 140), 
            ('TIKKA ( 8 PCS )', 150)
        ],
        'MALAI SPECIAL': [
            ('LEG PIECE ( 1 PCS )', 90), 
            ('LOLLIPOP ( 4 PCS )', 140), 
            ('WINGS ( 5 PCS )', 150), 
            ('TIKKA ( 8 PCS )', 160)
        ]
    }
    
    # Standard 3
    for cat_name, items in specials_data.items():
        cat = Category.objects.create(name=cat_name)
        print(f"Created Category: {cat_name}")
        for item_name, price in items:
            MenuItem.objects.create(category=cat, name=item_name, price=price)
            print(f"  - {item_name}: {price}")

    # Combos
    combo_cat = Category.objects.create(name="COMBOS")
    print("Created Category: COMBOS")
    
    MenuItem.objects.create(category=combo_cat, name="MEDIUM COMBO", price=399)
    print("  - MEDIUM COMBO: 399")
    
    MenuItem.objects.create(category=combo_cat, name="LARGE COMBO", price=599)
    print("  - LARGE COMBO: 599")

    print("\n--- Reset Complete. Database is clean. ---")

if __name__ == "__main__":
    reset_specials()
