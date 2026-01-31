from django.db import migrations
from django.db.models import Count

def deduplicate_items(apps, schema_editor):
    MenuItem = apps.get_model('orders', 'MenuItem')
    
    # Identify duplicates
    duplicates = MenuItem.objects.values('category', 'name').annotate(count=Count('id')).filter(count__gt=1)
    
    print(f"\n    Found {len(duplicates)} duplicate menu items.")
    
    for entry in duplicates:
        category_id = entry['category']
        name = entry['name']
        
        items = list(MenuItem.objects.filter(category_id=category_id, name=name))
        
        # Keep the first one, delete the rest
        primary = items[0]
        copies = items[1:]
        
        print(f"    Processing '{name}': Keeping ID {primary.id}, deleting {len(copies)} copies.")
        
        for copy in copies:
            copy.delete()

def reverse_code(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_category_name'),
    ]

    operations = [
        migrations.RunPython(deduplicate_items, reverse_code),
    ]
