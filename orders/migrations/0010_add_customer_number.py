from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_menuitem_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
