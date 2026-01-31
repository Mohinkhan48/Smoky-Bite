
import os
import django
import sys

# Ensure we're in the right directory
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

def populate():
    print("Starting population...")
    # Data Structure
    menu = {
        'MOMOS MENU': [
            ('CKN STEEM MOMOS', 60),
            ('CKN FRIED MOMOS', 70),
            ('CKN PERI PERI FRIED MOMOS', 70),
        ],
        'BURGER': [
            ('CKN BURGER', 79),
            ('CKN CHEESE BURGER', 99),
            ('CKN ZINGER BURGER', 110),
        ],
        'BROASTED & FRIES': [
            ('BROASTED CHICKEN (4 PCS)', 149),
            ('PERI PERI FRENCH FRIES', 70),
            ('SALTED FRENCH FRIES', 70),
        ],
        'HOT & CRISPY': [
            ('CKN CHEESE BALLS (5 PCS)', 79),
            ('CKN CRISPY STRIPS (5 PCS)', 79),
            ('CKN NUGGETS (5 PCS)', 79),
            ('CKN CRISPY POPCORN', 79),
        ],
        'MOCKTAILS': [
            ('BLUE ANGEL', 49),
            ('LIME MINT', 49),
            ('BLUEBERRY', 49),
            ('GINGER LIME', 49),
        ],
        'HOT & SPICY': [
            ('LEG PIECE (1 PCS)', 70),
            ('LOLLIPOP (4 PCS)', 120),
            ('WINGS (5 PCS)', 130),
            ('TIKKA (8 PCS)', 140),
        ],
        'PERI PERI': [
            ('LEG PIECE (1 PCS)', 80),
            ('LOLLIPOP (4 PCS)', 130),
            ('WINGS (5 PCS)', 140),
            ('TIKKA (8 PCS)', 150),
        ],
        'MALAI SPECIAL': [
            ('LEG PIECE (1 PCS)', 90),
            ('LOLLIPOP (4 PCS)', 140),
            ('WINGS (5 PCS)', 150),
            ('TIKKA (8 PCS)', 160),
        ],
        'COMBOS': [
            ('MEDIUM COMBO 399', 399),
            ('LARGE COMBO 599', 599),
        ]
    }

    try:
        # Clear existing
        Category.objects.all().delete()
        MenuItem.objects.all().delete()

        print("Cleared DB.")

        for cat_name, items in menu.items():
            category = Category.objects.create(name=cat_name)
            print(f"Created Category: {cat_name}")
            for item_name, price in items:
                MenuItem.objects.create(category=category, name=item_name, price=price)
                
        print("Done!")
        
        # Verify
        with open("populate_status.txt", "w") as f:
            f.write(f"Categories: {Category.objects.count()}\n")
            f.write(f"Items: {MenuItem.objects.count()}\n")
            
    except Exception as e:
        with open("populate_error.txt", "w") as f:
            f.write(str(e))
        print(f"Error: {e}")

if __name__ == '__main__':
    populate()
