from django.urls import include, path
from core.views import *

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    # path("<cat_title>/", category, name="category"),
    path("category/<str:cate_slug>/", category, name="inner-category"),
    path("shop-category/<str:main_slug>/", main_category, name="main_category"),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("product/<slug:product_slug>/", product, name="product"),
    path("product/<title>/", producttitle, name="producttitle"),
    path("search/", search_view, name="search"),
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    path("update-cart/", update_cart, name="update-cart"),
    path("checkout/", checkout_view, name="checkout"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path("payment-completed/", payment_completed_view, name="payment-completed"),
    path("payment-failed/", payment_failed_view, name="payment-failed"),
    path("architectures/", arch, name="arch"),
    path("architectures/<name>/", arch_name, name="arch_name"),
    path("builder/", build, name="build"),
    path("builder/<name>/", build_name, name="build_name"),
    path("about-us/", about, name="about-us"),
    path("our-reviews/", our_reviews, name="our-reviews"),
    path("our-clients/", our_clients, name="our-clients"),
    path("our-achievements/", our_achievements, name="our-achievements"),
    path("premium-websites/", premium_websites, name="premium-websites"),
    path("our-works/", our_works, name="our_works"),
    path("our-media/", our_media, name="our_media"),
    path("blog_details/<blog_slug>/", blog_details, name="blog_details"),
    path("contact-us/", contact, name="contact-us"),
    path("career", career, name="career"),
    path("write-to-ceo/", write_to_ceo, name="write_to_ceo"),
    path("blog/", blogs, name="blogs"),
    path("privacy-policy/", privacypolicy, name="privacypolicy"),
    path("<slug:sub_cat_slug>/", sub_category, name="sub-category"),
]
