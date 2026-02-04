
from django.db import migrations

def fix_legacy_paths(apps, schema_editor):
    MenuItem = apps.get_model('orders', 'MenuItem')
    
    # Map keywords/substrings to the correct static file
    # key: substring to look for, value: correct static path
    keyword_map = {
        'momos': 'img/Momos.png',
        'burger': 'img/Burgerimage.png',
        'brost': 'img/Brost.png',
        'crispy': 'img/Hotcrispy.png',
        'popcorn': 'img/Hotcrispy.png',
        'nuggets': 'img/Hotcrispy.png',
        'strips': 'img/Hotcrispy.png',
        'balls': 'img/Hotcrispy.png',
        'medium': 'img/Mediumcombo.png', # for combos
        'large': 'img/Largecombo.png',   # for combos
        'mocktail': 'img/Mocktails.png',
        'blue': 'img/Mocktails.png',
        'lime': 'img/Mocktails.png',
        'ginger': 'img/Mocktails.png',
        'wings': 'img/Brost.png',
        'tikka': 'img/Brost.png',
        'lollipop': 'img/Brost.png',
        'leg piece': 'img/Brost.png',
    }

    count = 0
    for item in MenuItem.objects.all():
        # Get current path and normalize
        current_path = str(item.image).lower()
        
        # If it's already correct, skip
        # Note: We check if it ENDS with the correct filename to avoid partial matches
        # But casing might differ, so we look for exact path match case-insensitive
        
        found_match = False
        
        # Fallback 1: Check known keywords in the Name or Path
        search_text = (current_path + " " + item.name.lower())
        
        for key, correct_path in keyword_map.items():
            if key in search_text:
                if item.image != correct_path:
                    print(f"Fixing {item.name}: '{item.image}' -> '{correct_path}'")
                    item.image = correct_path
                    item.save()
                    count += 1
                found_match = True
                break
        
        # If no match found using keywords, force default if it looks like a legacy path
        if not found_match and 'menu_items' in current_path:
             print(f"Resetting unknown legacy item {item.name} to placeholder")
             item.image = 'img/placeholder.png'
             item.save()
             count += 1

    print(f"Fixed {count} legacy items.")

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_production_fix'),
    ]

    operations = [
        migrations.RunPython(fix_legacy_paths),
    ]
