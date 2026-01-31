import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

def force_populate():
    specials_data = {
        'HOT & SPICY': [('LEG PIECE ( 1 PCS )', 70), ('LOLLIPOP ( 4 PCS )', 120), ('WINGS ( 5 PCS )', 130), ('TIKKA ( 8 PCS )', 140)],
        'PERI PERI': [('LEG PIECE ( 1 PCS )', 80), ('LOLLIPOP ( 4 PCS )', 130), ('WINGS ( 5 PCS )', 140), ('TIKKA ( 8 PCS )', 150)],
        'MALAI SPECIAL': [('LEG PIECE ( 1 PCS )', 90), ('LOLLIPOP ( 4 PCS )', 140), ('WINGS ( 5 PCS )', 150), ('TIKKA ( 8 PCS )', 160)]
    }

    print("--- Force Populating Specials ---")

    for cat_name, items in specials_data.items():
        cat, created = Category.objects.get_or_create(name=cat_name)
        print(f"Category: {cat.name} (Created: {created})")
        
        # Clear existing
        count_before = cat.items.count()
        cat.items.all().delete()
        print(f"  Deleted {count_before} items")
        
        for name, price in items:
            MenuItem.objects.create(category=cat, name=name, price=price)
        print(f"  Added {len(items)} items")

    # Combos
    combo_cat, _ = Category.objects.get_or_create(name="COMBOS")
    combo_cat.items.all().delete()
    MenuItem.objects.create(category=combo_cat, name="MEDIUM COMBO", price=399)
    MenuItem.objects.create(category=combo_cat, name="LARGE COMBO", price=599)
    print("Combos updated.")
    
if __name__ == "__main__":
    force_populate()
