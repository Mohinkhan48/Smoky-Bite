import os
import django
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoky_bites.settings')
django.setup()

from orders.models import Category

def deduplicate():
    print("Scanning for duplicate categories...")
    
    # Find names that have more than 1 entry
    duplicates = Category.objects.values('name').annotate(count=Count('id')).filter(count__gt=1)
    
    if not duplicates:
        print("No duplicates found.")
        return

    for entry in duplicates:
        name = entry['name']
        count = entry['count']
        print(f"Found {count} copies of '{name}'")
        
        # Get all instances
        cats = list(Category.objects.filter(name=name))
        
        # Keep the first one, delete the rest
        original = cats[0]
        copies = cats[1:]
        
        for copy in copies:
            # Move items to the original category
            items_moved = copy.items.update(category=original)
            print(f"  - Moved {items_moved} items from copy ID {copy.id} to original ID {original.id}")
            
            print(f"  - Deleting copy ID {copy.id}")
            copy.delete()
            
    print("Deduplication complete.")

if __name__ == "__main__":
    deduplicate()
