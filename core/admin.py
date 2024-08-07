from django.contrib import admin
from core.models import *
import csv
from django.urls import path
from django.http import HttpResponse
from django.utils.html import format_html
from core.forms import ExportCartOrdersForm
from core.views import *

class ProductSeoAdmin(admin.StackedInline):
    model = ProductSeo
    extra = 0
    fields = (
        'canonical_link',
        'meta_description',
        'meta_title',
        'meta_tag',
        'meta_robots',
        'og_url',
        'og_title',
        'og_description',
        'og_image',
        'twitter_title',
        'twitter_description',
    )

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 0

class ArchitectureImagesAdmin(admin.TabularInline):
    model = ArchitectureImages

class BuilderImagesAdmin(admin.TabularInline):
    model = BuilderImages
    extra = 0



class WorkImagesAdmin(admin.TabularInline):
    model = WorksImages
    extra = 0

class ProductVariantImagesAdmin(admin.StackedInline):
    model = ProductVariantImages
    extra = 0  # This allows adding multiple images at once in the admin

class ProductVarientAdmin(admin.StackedInline):
    model = ProductVarient
    extra = 0
    inlines = [ProductVariantImagesAdmin]

class SubCategoryImagesAdmin(admin.TabularInline):
    model = SubcategoryImages
    extra = 3  # This allows adding multiple images at once in the admin



class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, ProductSeoAdmin, ProductVarientAdmin, ProductVariantImagesAdmin]
    list_display = ['company_name', 'main_category', 'category', 'sub_category', 'title', 'product_slug', 'price', 'featured', 'product_status']
    list_filter = ['company_name', 'main_category', 'category', 'sub_category', 'featured', 'product_status']  # Add fields you want to filter by
    search_fields = ['title', 'description']  # Add fields you want to search by

class ArchitectureAdmin(admin.ModelAdmin):
    inlines = [ArchitectureImagesAdmin]
    list_display = ['name', 'contact', 'email', 'address', 'description', 'instagram', 'facebook', 'linkedin', 'twitter', 'featured']
    list_filter = ['name', 'featured', 'contact', 'address', 'email']  # Add fields you want to filter by
    search_fields = ['title', 'description']  # Add fields you want to search by


class BuilderAdmin(admin.ModelAdmin):
    inlines = [BuilderImagesAdmin]
    list_display = ['name', 'contact', 'email', 'address', 'description', 'instagram', 'facebook', 'linkedin', 'twitter', 'featured']
    list_filter = ['name', 'featured', 'contact', 'address', 'email']  # Add fields you want to filter by
    search_fields = ['title', 'description']  # Add fields you want to search by

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['main_title', 'meta_description', 'meta_title', 'meta_tag', 'image', 'icon_img']     

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['main_category', 'cat_title', 'meta_description', 'meta_title', 'meta_tag', 'image', 'big_image']
    list_filter = ['main_category']  # Fields to filter by

class CompanyNameAdmin(admin.ModelAdmin):
    list_display = ['maincat', 'category', 'sub_category', 'company_name_title', 'user', 'ecommerce', 'meta_description', 'image']
    list_filter = ['maincat', 'category', 'sub_category']  # Add fields you want to filter by
    search_fields = ['company_name_title', 'meta_description', 'meta_title', 'meta_tag']


class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryImagesAdmin]
    list_display = ['maincat', 'category', 'sub_cat_title', 'slug', 'user', 'page_about_description', 'youtube_link', 'image']
    list_filter = ['maincat', 'category']  # Add fields you want to filter by
    search_fields = ['sub_cat_title', 'meta_description', 'meta_title']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status', 'tracking_id']
    list_display = ['firstname', 'zipcode', 'price', 'paid_status', 'order_date', 'tracking_id', 'product_status', 'download_invoice_link']
    list_filter = ['tracking_id', 'phone', 'email', 'zipcode', 'firstname', 'courier_partner']
    search_fields = ['tracking_id', 'phone', 'email', 'zipcode', 'firstname', 'lastname', 'city', 'billingaddress', 'shippingaddress', 'courier_partner'] 
    change_list_template = "core/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/', self.admin_site.admin_view(self.export_cart_orders_csv), name='export_cart_orders_csv'),
            path('<int:order_id>/invoice/', self.admin_site.admin_view(generate_invoice), name='generate_invoice'),
        ]
        return custom_urls + urls

    def download_invoice_link(self, obj):
        return format_html('<a class="btn btn-success" href="{}">Download Invoice</a>', reverse('admin:generate_invoice', args=[obj.id]))

    download_invoice_link.short_description = 'Download Invoice'
    download_invoice_link.allow_tags = True

    def export_cart_orders_csv(self, request):
        form = ExportCartOrdersForm(request.GET)
        if form.is_valid():
            orders = CartOrder.objects.all()
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            paid_status = form.cleaned_data.get('paid_status')

            if start_date and end_date:
                orders = orders.filter(order_date__range=[start_date, end_date])
            elif start_date:
                orders = orders.filter(order_date__gte=start_date)
            elif end_date:
                orders = orders.filter(order_date__lte=end_date)

            if paid_status:
                orders = orders.filter(paid_status=(paid_status == 'True'))

        else:
            orders = CartOrder.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cart_orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['Price', 'Courier Partner', 'Tracking ID', 'Paid Status', 'Order Date', 'Product Status',
                         'First Name', 'Last Name', 'Zip Code', 'City', 'District', 'Division', 'State',
                         'Billing Address', 'Shipping Address', 'Phone', 'Email'])

        for order in orders.values_list('price', 'courier_partner', 'tracking_id', 'paid_status', 'order_date', 'product_status',
                                        'firstname', 'lastname', 'zipcode', 'city', 'district', 'division', 'state',
                                        'billingaddress', 'shippingaddress', 'phone', 'email'):
            writer.writerow(order)

        return response


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']


class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['privacy_policy_content']     

class BlogsAdmin(admin.ModelAdmin):
    list_display = ['blog_title', 'blog_image', 'blog_description']      


class WorkAdmin(admin.ModelAdmin):
    inlines = [WorkImagesAdmin]
    list_display = ['category_title', 'status', 'order']
    list_filter = ['category_title', 'status']  # Add fields you want to filter by
    search_fields = ['category_title', 'status']  # Add fields you want to search by

class MediaAdmin(admin.ModelAdmin):
    list_display = ['media_address', 'status']
    list_filter = ['media_address', 'status']  # Add fields you want to filter by
    search_fields = ['media_address', 'status']  # Add fields you want to search by

admin.site.register(Product, ProductAdmin)
admin.site.register(Architecture, ArchitectureAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(Main_category, MainCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Company_name, CompanyNameAdmin)
admin.site.register(Sub_categories, SubCategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Works, WorkAdmin)
admin.site.register(Media, MediaAdmin)
