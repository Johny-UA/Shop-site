# Generated by Django 5.0.3 on 2024-04-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_alter_product_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='purchase_is_returned',
            field=models.BooleanField(default=False),
        ),
    ]
