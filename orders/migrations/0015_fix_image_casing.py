
from django.db import migrations

def fix_image_paths(apps, schema_editor):
    MenuItem = apps.get_model('orders', 'MenuItem')
    
    # Exact case mapping for Linux/Railway
    mapping = {
        'img/momos.png': 'img/Momos.png',
        'img/burgerimage.png': 'img/Burgerimage.png',
        'img/brost.png': 'img/Brost.png',
        'img/hotcrispy.png': 'img/Hotcrispy.png',
        'img/mediumcombo.png': 'img/Mediumcombo.png',
        'img/largecombo.png': 'img/Largecombo.png',
        'img/mocktails.png': 'img/Mocktails.png',
    }

    for item in MenuItem.objects.all():
        current = str(item.image).lower().replace('\\', '/') # Normalize
        
        # Check standard mapping
        if current in mapping:
            if item.image != mapping[current]:
                print(f"Migrating {item.name}: {item.image} -> {mapping[current]}")
                item.image = mapping[current]
                item.save()
        
        # Fallback: Force known filenames if containment matches
        # This handles cases like 'img/burgerimage.png' -> 'img/Burgerimage.png' 
        # even if not exact match in dict, but let's be safe with direct mapping first.
        
        # Also ensure simple "Momos.png" -> "img/Momos.png"
        if not str(item.image).startswith('img/'):
            # Try to save it
            pass 

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_remove_order_delivery_status_alter_order_status'),
    ]

    operations = [
        migrations.RunPython(fix_image_paths),
    ]
