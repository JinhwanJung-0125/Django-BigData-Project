# Generated by Django 4.2.1 on 2023-05-24 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_housetable_idx_housetable_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housetable',
            old_name='id',
            new_name='idx',
        ),
    ]
