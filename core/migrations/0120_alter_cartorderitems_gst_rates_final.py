# Generated by Django 4.2.4 on 2024-08-07 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0119_delete_productreview"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorderitems",
            name="gst_rates_final",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=99999),
        ),
    ]