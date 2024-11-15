from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from unicodedata import decimal
from pyexpat import model
from email.policy import default
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.urls import reverse


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

COURIER_PARTNER = (
    ("not assigned", "NOT ASSIGNED"),
    ("dtdc", "DTDC"),
    ("trackon", "Trackon"),
)

WORK_STATUS = (
    ("disabled", "Disabled"),
    ("published", "Published"),
)

RATING = (
    ("1", "★"),
    ("2", "★★"),
    ("3", "★★★"),
    ("4", "★★★★"),
    ("5", "★★★★★"),
)

COLOR = (
    ("red", "Red"),
    ("black", "Black"),
    ("pink", "Pink"),
    ("blue", "Blue"),
    ("orange", "Orange"),
)

def user_directory_path(instance, filename):
    user_id = instance.user.id if instance.user else 'unknown'
    return 'user_{0}/{1}'.format(user_id, filename)

class Main_category(models.Model):
    mid = ShortUUIDField(unique=True, max_length=30, prefix="main_cat", alphabet="abcdefgh12345")
    main_title = models.CharField(max_length=100)
    main_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category",default="maincategory.jpg")
    icon_img = models.ImageField(upload_to="categoryicon",default="maincategoryicon.jpg")

    class Meta:
        verbose_name_plural = "Main Categories"

    def main_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_category_icon_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.icon_img.url))
    
    def save(self, *args, **kwargs):
        if not self.main_slug:
            self.main_slug = slugify(self.main_title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:main_category', kwargs={'main_slug': str(self.main_slug)})
    
    def __str__(self):
        return self.main_title


class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    cat_title = models.CharField(max_length=100, default="Mobile & Laptop")
    cate_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default="category.jpg")
    big_image = models.ImageField(upload_to=user_directory_path, default="bigcategory.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def category_big_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.big_image.url))
    
    def save(self, *args, **kwargs):
        if not self.cate_slug:
            self.cate_slug = slugify(self.cat_title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:inner-category', kwargs={'cate_slug': str(self.cate_slug)})
    
    def __str__(self):
        return self.cat_title


class Tags(models.Model):
    pass    

class Sub_categories(models.Model):
    ssid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345")   
    maincat = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sub_cat_title = models.CharField(max_length=100, default="Mobile & Laptop")
    slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    description = models.CharField(max_length=200)
    page_about_description = models.CharField(max_length=500)
    bottom_page_description = HTMLField()
    canonical_link = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200)
    meta_tag = models.CharField(max_length=200)
    meta_robots = models.CharField(max_length=100)
    og_url = models.CharField(max_length=100)
    og_title = models.CharField(max_length=100)
    og_description = models.CharField(max_length=100)
    og_image = models.CharField(max_length=100)
    twitter_title = models.CharField(max_length=100)
    twitter_description = models.CharField(max_length=100)
    twitter_description = models.CharField(max_length=100)
    youtube_link = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=user_directory_path, default="subcategory.jpg")
    main_page_img = models.ImageField(upload_to=user_directory_path, default="mainpageimg.jpg")

    class Meta:
        verbose_name_plural = "Sub Categories"

    def sub_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_page_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.main_page_img.url))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.sub_cat_title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:sub-category', kwargs={'sub_cat_slug': str(self.slug)})
    
    def __str__(self):
        return self.sub_cat_title
    

class SubcategoryImages(models.Model):
    images = models.ImageField(upload_to="sub-categories-images", default="sub-category.jpg")
    sub_category = models.ForeignKey(Sub_categories, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Sub Categories Images"

    
class Company_name(models.Model):
    sid = ShortUUIDField(unique=True, max_length=50, prefix="Company_name", alphabet="abcdefgh12345")   
    maincat = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(Sub_categories, on_delete=models.SET_NULL, null=True)
    company_name_title = models.CharField(max_length=100, default="Mobile & Laptop")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    ecommerce = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    curtain_fabric_category = models.BooleanField(default=False)
    fabric_use_upholstery_category = models.BooleanField(default=False)
    window_blinds_category = models.BooleanField(default=False)
    wall_panel_category = models.BooleanField(default=False)
    wallpaper_category = models.BooleanField(default=False)
    curtain_sofa_brands = models.BooleanField(default=False)
    mattresses_brands = models.BooleanField(default=False)
    window_blinds_brands = models.BooleanField(default=False)
    carpet_tile_for_office_brands = models.BooleanField(default=False)
    carpet_rolls_brands = models.BooleanField(default=False)
    rugs_brands = models.BooleanField(default=False)
    pillow_brands = models.BooleanField(default=False)
    hospital_walls_brands = models.BooleanField(default=False)
    wooden_laminate_flooring_brands = models.BooleanField(default=False)
    pvc_rubber_flooring_brands = models.BooleanField(default=False)
    curtains_rods_channel_brands = models.BooleanField(default=False)
    foam_material_brands = models.BooleanField(default=False)
    awning_canopy_brands = models.BooleanField(default=False)
    image = models.ImageField(upload_to=user_directory_path, default="subcategory.jpg")
    main_page_img = models.ImageField(upload_to=user_directory_path, default="mainpageimg.jpg")
    logo_img = models.ImageField(upload_to=user_directory_path, default="logo.jpg")

    class Meta:
        verbose_name_plural = "Company Name"

    def sub_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_page_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.main_page_img.url))
    
    def logo_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.logo_img.url))
    
    def __str__(self):
        return self.company_name_title
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345")
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(Sub_categories, on_delete=models.SET_NULL, null=True)
    company_name = models.ForeignKey(Company_name, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, default="Mobile & Laptop")
    product_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True, default="This is the product")
    bottom_page_description = HTMLField(default="N/A")
    price = models.DecimalField(max_digits=9999, decimal_places=2, default="1")
    old_price = models.DecimalField(max_digits=9999, decimal_places=2, default="2")
    gst_rate = models.CharField(max_length=100, default="18")
    specifications = models.TextField(max_length=500,null=True, blank=True, default="N/A")
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    color = models.CharField(choices=COLOR, max_length=10, default="black")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")
    deposit_desc = models.TextField(max_length=500, null=True, blank=True, default="On Demand Deposit") 
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")

    class Meta:
        verbose_name_plural = "Product"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.product_slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            # Loop to find a unique slug
            while Product.objects.filter(product_slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.product_slug = unique_slug

        super().save(*args, **kwargs) 

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'product_slug': self.product_slug})
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"

class ProductSeo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    canonical_link = models.CharField(max_length=500, default="N/A")
    meta_description = models.CharField(max_length=500, default="N/A")
    meta_title = models.CharField(max_length=500, default="N/A")
    meta_tag = models.CharField(max_length=500, default="N/A")
    meta_robots = models.CharField(max_length=500, default="N/A")
    og_url = models.CharField(max_length=500, default="N/A")
    og_title = models.CharField(max_length=500, default="N/A")
    og_description = models.CharField(max_length=500, default="N/A")
    og_image = models.CharField(max_length=500, default="N/A")
    twitter_title = models.CharField(max_length=500, default="N/A")
    twitter_description = models.CharField(max_length=500, default="N/A")
    twitter_description = models.CharField(max_length=500, default="N/A")


    class Meta:
        verbose_name_plural = "Product Seo"


class ProductVarient(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345") 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, default="productvarient.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, default="Product Varient")
    description = models.TextField(max_length=500, null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="2.99")
    specifications = models.TextField(max_length=500, null=True, blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    color = models.CharField(choices=COLOR, max_length=10, default="black")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Varient"

    def variant_images(self):
        return ProductVariantImages.objects.filter(product_variant=self)
    
    def __str__(self):
        return self.title

    def product_varient_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    

class ProductVariantImages(models.Model):
    product_variant = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, default="productvarient.jpg")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Variant Images"

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    courier_partner = models.CharField(choices=COURIER_PARTNER, max_length=30, default="Not Assigned")
    tracking_id = models.CharField(max_length=100, default="N/A")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    pin_details = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    division = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    billingaddress = models.CharField(max_length=200, blank=True, null=True)
    shippingaddress = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    companyname = models.CharField(max_length=200, blank=True, null=True)
    gstnumber = models.CharField(max_length=200, blank=True, null=True)
    price_wo_gst_total = models.DecimalField(max_digits=99999, decimal_places=2, default="0")
    gst_rates_final = models.DecimalField(max_digits=99999, decimal_places=2, default="0.00")  # For storing the GST rate

    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    total = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    price_wo_gst = models.DecimalField(max_digits=99999, decimal_places=2, default="0")  # Update field name
    gst_rates_final = models.DecimalField(max_digits=99999, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image.url))


class Architecture(models.Model):
    aid = ShortUUIDField(unique=True, max_length=30, prefix="arch", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, default="CJS BHATIA...")
    contact = models.CharField(max_length=100, default="+91-")
    email = models.CharField(max_length=100, default="@gmail.com")
    address = models.CharField(max_length=100, default="South Delhi...")
    description = models.TextField(null=True, blank=True, default="about yourself...")
    instagram = models.CharField(max_length=100, default="@instagram.com")
    facebook = models.CharField(max_length=100, default="@facebook.com")
    linkedin = models.CharField(max_length=100, default="@linkedin.com")
    twitter = models.CharField(max_length=100, default="@twitter.com")
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default="architecture.jpg")

    class Meta:
        verbose_name_plural = "Architecture"

    def arch_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.name
    
class ArchitectureImages(models.Model):
    location = models.CharField(max_length=100, default="south ex..")
    images = models.ImageField(upload_to="architecture-images", default="architecture.jpg")
    architecture = models.ForeignKey(Architecture, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Architecture Project Images"

class PrivacyPolicy(models.Model):
    privacy_policy_content = HTMLField()


    class Meta:
        verbose_name_plural = "Privacy Policy"


class Builder(models.Model):
    bid = ShortUUIDField(unique=True, max_length=30, prefix="build", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, default="CJS BHATIA...")
    contact = models.CharField(max_length=100, default="+91-")
    email = models.CharField(max_length=100, default="@gmail.com")
    address = models.CharField(max_length=100, default="South Delhi...")
    description = models.TextField(null=True, blank=True, default="about yourself...")
    instagram = models.CharField(max_length=100, default="@instagram.com")
    facebook = models.CharField(max_length=100, default="@facebook.com")
    linkedin = models.CharField(max_length=100, default="@linkedin.com")
    twitter = models.CharField(max_length=100, default="@twitter.com")
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default="builder.jpg")

    class Meta:
        verbose_name_plural = "Builder"

    def arch_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def _str_(self):
        return self.name



class BuilderImages(models.Model):
    location = models.CharField(max_length=100, default="south ex..")
    images = models.ImageField(upload_to="architecture-images", default="architecture.jpg")
    builder = models.ForeignKey(Builder, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Builder Project Images"

class InvoiceNumber(models.Model):
    number = models.IntegerField(default=1)

    def increment(self):
        self.number += 1
        self.save()

    def __str__(self):
        return f'TPH2024-{self.number:04d}'



class Blogs(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_image = models.ImageField(upload_to="blogs-images", default="blogs.jpg")
    blog_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True) 
    blog_description = HTMLField()
    permalink = models.CharField(max_length=500)
    meta_description = models.CharField(max_length=500)
    focus_keyword = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Blogs"

class Works(models.Model):
    wid = ShortUUIDField(unique=True, max_length=12, prefix="our_works", alphabet="abcdefgh12345")
    category_title = models.CharField(max_length=100, default="Wallpapers")
    status = models.CharField(choices=WORK_STATUS, max_length=10, default="published")
    order = models.PositiveIntegerField(default=0)  # New field to define the order

    class Meta:
        verbose_name_plural = "Our Work"
        ordering = ['order']  # Default ordering by the order field

    def _str_(self):
        return self.category_title
    
class WorksImages(models.Model):
    address = models.CharField(max_length=100, blank=True)
    brand_name = models.CharField(max_length=100, blank=True)
    link_to_brand = models.CharField(max_length=100, blank=True)
    images = models.ImageField(upload_to="product-images", default="work_images.jpg")
    works = models.ForeignKey(Works, on_delete=models.SET_NULL, null=True)
    videos = models.FileField(upload_to="product-videos", default="work_videos.mp4", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Our Work Images"

class Media(models.Model):
    mid = ShortUUIDField(unique=True, max_length=31, prefix="our_works", alphabet="abcdefgh12345")
    media_address = models.CharField(max_length=100, default="Ring Road...")
    images = models.ImageField(upload_to="product-images", default="media_images.jpg")
    status = models.CharField(choices=WORK_STATUS, max_length=10, default="published")

    class Meta:
        verbose_name_plural = "Our Media"
    
    def _str_(self):
        return self.media_address


