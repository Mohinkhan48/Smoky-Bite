
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

    count = 0
    for item in MenuItem.objects.all():
        current = item.image.lower().replace('\\', '/') # Normalize
        
        # Check standard mapping
        if current in mapping:
            if item.image != mapping[current]:
                print(f"Migrating {item.name}: {item.image} -> {mapping[current]}")
                item.image = mapping[current]
                item.save()
                count += 1
        
        # Fallback for Momos specifically if strict mapping failed
        if 'momos' in current and 'img/momos.png' not in item.image:
             pass 

    print(f"Fixed {count} items.")

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_correct_image_casing'),
    ]

    operations = [
        migrations.RunPython(fix_image_paths),
    ]
