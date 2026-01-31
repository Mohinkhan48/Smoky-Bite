import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

def master_populate():
    print("Starting population...")
    
    # Page 1
    front_menu = {
        'MOMOS MENU': [('CKN STEEM MOMOS', 60), ('CKN FRIED MOMOS', 70), ('CKN PERI PERI FRIED MOMOS', 70)],
        'BURGER': [('CKN BURGER', 79), ('CKN CHEESE BURGER', 99), ('CKN ZINGER BURGER', 110)],
        'BROASTED & FRIES': [('BROASTED CHICKEN (4 PCS)', 149), ('PERI PERI FRENCH FRIES', 70), ('SALTED FRENCH FRIES', 70)],
        'HOT & CRISPY': [('CKN CHEESE BALLS (5 PCS)', 79), ('CKN CRISPY STRIPS (5 PCS)', 79), ('CKN NUGGETS (5 PCS)', 79), ('CKN CRISPY POPCORN', 79)],
        'MOCKTAILS': [('BLUE ANGEL', 49), ('LIME MINT', 49), ('BLUEBERRY', 49), ('GINGER LIME', 49)]
    }
    
    # Page 2
    specials_menu = {
        'HOT & SPICY': [('LEG PIECE ( 1 PCS )', 70), ('LOLLIPOP ( 4 PCS )', 120), ('WINGS ( 5 PCS )', 130), ('TIKKA ( 8 PCS )', 140)],
        'PERI PERI': [('LEG PIECE ( 1 PCS )', 80), ('LOLLIPOP ( 4 PCS )', 130), ('WINGS ( 5 PCS )', 140), ('TIKKA ( 8 PCS )', 150)],
        'MALAI SPECIAL': [('LEG PIECE ( 1 PCS )', 90), ('LOLLIPOP ( 4 PCS )', 140), ('WINGS ( 5 PCS )', 150), ('TIKKA ( 8 PCS )', 160)],
        'COMBOS': [('MEDIUM COMBO', 399), ('LARGE COMBO', 599)]
    }

    # Combine all
    all_menu = {**front_menu, **specials_menu}
    
    for cat_name, items in all_menu.items():
        cat, created = Category.objects.get_or_create(name=cat_name)
        for name, price in items:
            item, i_created = MenuItem.objects.get_or_create(
                category=cat, 
                name=name, 
                defaults={'price': price}
            )
            if not i_created:
                item.price = price
                item.save()
    
    print("Population/Update complete.")

if __name__ == "__main__":
    master_populate()
