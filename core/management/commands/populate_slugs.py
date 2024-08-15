from django.core.management.base import BaseCommand
from core.models import Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate slugs for products that do not have a slug or have a duplicate slug'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            if not product.product_slug or Product.objects.filter(product_slug=product.product_slug).exclude(pk=product.pk).exists():
                base_slug = slugify(product.title)
                unique_slug = base_slug
                counter = 1

                # Loop to find a unique slug
                while Product.objects.filter(product_slug=unique_slug).exists():
                    unique_slug = f"{base_slug}-{counter}"
                    counter += 1

                product.product_slug = unique_slug
                product.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated slugs'))
