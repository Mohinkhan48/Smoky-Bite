import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category, MenuItem

def update_content():
    # 1. Update Categories
    cat_updates = {
        "Momos": "MOMOS MENU",
        "Burger": "BURGER",
        "Broasted Chicken": "BROASTED + FRIES",
        "Hot & Crispy": "HOT + CRISPY"
    }
    
    for old_name, new_name in cat_updates.items():
        try:
            cat = Category.objects.get(name__iexact=old_name)
            cat.name = new_name
            cat.save()
            print(f"Updated Category: {old_name} -> {new_name}")
        except Category.DoesNotExist:
            print(f"Category not found: {old_name}")

    # 2. Update Items
    item_updates = {
        "Steam Momos": "CKN STEEM MOMOS",
        "Fried Momos": "CKN FRIED MOMOS",
        "Peri Peri Fried Momos": "CKN PERI PERI FRIED MOMOS",
        "Chicken Burger": "CKN BURGER",
        "Chicken Cheese Burger": "CKN CHEESE BURGER",
        "Zinger Burger": "CKN ZINGER BURGER",
        # Add any others from the image if visible, or general "Chicken" -> "CKN" rule
    }

    for item in MenuItem.objects.all():
        original_name = item.name
        new_name = original_name
        
        # Exact title updates
        for old_start, new_start in item_updates.items():
            if item.name.lower() == old_start.lower():
                new_name = new_start
                break
        
        # General replacement if not exact match (optional, but safer to stick to list first)
        if "Chicken" in new_name and "CKN" not in new_name:
             new_name = new_name.replace("Chicken", "CKN")

        if new_name != original_name:
            item.name = new_name
            item.save()
            print(f"Updated Item: {original_name} -> {new_name}")

if __name__ == "__main__":
    update_content()
