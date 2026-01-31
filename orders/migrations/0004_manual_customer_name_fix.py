import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_name',
            field=models.CharField(default='Guest', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=40, unique=True),
        ),
    ]
