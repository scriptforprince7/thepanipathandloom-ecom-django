# Generated by Django 4.2.4 on 2024-06-20 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0106_alter_product_caution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='caution',
            new_name='deposit',
        ),
    ]
