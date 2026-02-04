
from django.db import migrations, models

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
        current = str(item.image).lower().replace('\\', '/')
        
        # Check standard mapping
        if current in mapping:
            # We must set it to the Mapped Value
            if str(item.image) != mapping[current]:
                print(f"Migrating {item.name}: {item.image} -> {mapping[current]}")
                item.image = mapping[current]
                item.save()
                count += 1
        else:
             # Ensure prefix
             if not str(item.image).startswith('img/'):
                 # It might be empty or pure filename
                 pass

    print(f"Fixed {count} items.")

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_fix_image_casing'),
    ]

    operations = [
        # 1. Convert ImageField to CharField (Schema Fix)
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.CharField(default='img/placeholder.png', max_length=200),
        ),
        # 2. Fix Data Casing (Data Fix)
        migrations.RunPython(fix_image_paths),
    ]
