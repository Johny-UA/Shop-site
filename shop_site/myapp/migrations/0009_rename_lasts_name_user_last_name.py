# Generated by Django 5.0.3 on 2024-03-26 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_user_first_name_user_lasts_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='lasts_name',
            new_name='last_name',
        ),
    ]
