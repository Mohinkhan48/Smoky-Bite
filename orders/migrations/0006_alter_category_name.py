from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_deduplicate_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
