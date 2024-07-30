# Generated by Django 4.2.4 on 2024-02-13 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0090_remove_productvarient_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productseo",
            name="canonical_link",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="meta_description",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="meta_robots",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="meta_tag",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="meta_title",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="og_description",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="og_image",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="og_title",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="og_url",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="twitter_description",
            field=models.CharField(default="N/A", max_length=500),
        ),
        migrations.AlterField(
            model_name="productseo",
            name="twitter_title",
            field=models.CharField(default="N/A", max_length=500),
        ),
    ]
