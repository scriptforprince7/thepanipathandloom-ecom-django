# Generated by Django 4.2.4 on 2024-08-16 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0122_remove_cartorder_billing_address_line1_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartorder",
            old_name="shipping_street_address",
            new_name="billingaddress",
        ),
        migrations.AddField(
            model_name="cartorder",
            name="shippingaddress",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
