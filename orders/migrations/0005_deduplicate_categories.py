from django.db import migrations
from django.db.models import Count

def deduplicate_categories(apps, schema_editor):
    Category = apps.get_model('orders', 'Category')
    MenuItem = apps.get_model('orders', 'MenuItem')
    
    # Identify duplicates
    duplicates = Category.objects.values('name').annotate(count=Count('id')).filter(count__gt=1)
    
    print(f"\n    Found {len(duplicates)} duplicate category names.")
    
    for entry in duplicates:
        name = entry['name']
        cats = list(Category.objects.filter(name=name))
        
        # Sort by ID (usually keep the oldest, or the one with items)
        # Here we just keep the first one found (usually oldest)
        primary = cats[0]
        copies = cats[1:]
        
        print(f"    Processing '{name}': Keeping ID {primary.id}, merging {len(copies)} copies.")
        
        for copy in copies:
            # Move all menu items from this copy to the primary
            # We use update() for efficiency and safety
            count = MenuItem.objects.filter(category=copy).update(category=primary)
            print(f"      - Moved {count} items from ID {copy.id} to ID {primary.id}")
            
            # Now safe to delete
            copy.delete()

def reverse_code(apps, schema_editor):
    # Cannot really reverse deduplication easily
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_manual_customer_name_fix'),
    ]

    operations = [
        migrations.RunPython(deduplicate_categories, reverse_code),
    ]
