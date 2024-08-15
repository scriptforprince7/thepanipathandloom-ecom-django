from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from core.models import *
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
import os
import requests
from django.db.models import Case, When, Value, IntegerField
from django.views.generic import View
import razorpay
from django.db import transaction
from decimal import Decimal, InvalidOperation
from datetime import datetime 
from decimal import Decimal, ROUND_HALF_UP
import re
from django.http import QueryDict
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags    
from num2words import num2words
from bs4 import BeautifulSoup
from indian_pincode_details import get_pincode_details
import indiapins
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from xhtml2pdf import pisa
from io import BytesIO


def index(request):
    product = Main_category.objects.all()
    walpaper_cat = Company_name.objects.filter(wallpaper_category=True)
    curtain_sofa_brands = Company_name.objects.filter(curtain_sofa_brands=True)
    mattresses_brands = Company_name.objects.filter(mattresses_brands=True)
    window_blind_brands = Company_name.objects.filter(window_blinds_brands=True)
    carpet_tile_office = Company_name.objects.filter(carpet_tile_for_office_brands=True)
    rugs_brands = Company_name.objects.filter(rugs_brands=True)
    pillow_brands = Company_name.objects.filter(pillow_brands=True)
    hospital_floor_walls = Company_name.objects.filter(hospital_walls_brands=True)
    wooden_laminate = Company_name.objects.filter(wooden_laminate_flooring_brands=True)
    pvc_rubber = Company_name.objects.filter(pvc_rubber_flooring_brands=True)
    curtain_rods_channel = Company_name.objects.filter(curtains_rods_channel_brands=True)
    foam_material = Company_name.objects.filter(foam_material_brands=True)
    awning_canopy = Company_name.objects.filter(awning_canopy_brands=True)


    context = {
        "main_cat":product,
        "walpaper_cat": walpaper_cat,
        "curtain_sofa_brands": curtain_sofa_brands,
        "mattresses_brands": mattresses_brands,
        "window_blind_brands": window_blind_brands,
        "carpet_tile_office": carpet_tile_office,
        "rugs_brands": rugs_brands,
        "pillow_brands": pillow_brands,
        "hospital_floor_walls": hospital_floor_walls,
        "wooden_laminate": wooden_laminate,
        "pvcrubber": pvc_rubber,
        "curtain_rods_channel": curtain_rods_channel,
        "foam_material": foam_material,
        "awning_canopy": awning_canopy,
    }
    return render(request, 'core/index.html', context)

def category(request, cate_slug):
    category = get_object_or_404(Category, cate_slug=cate_slug)
    company_names = Company_name.objects.filter(category=category)
    
    # Fetch all sub-categories related to the category
    all_sub_categories = Sub_categories.objects.filter(category=category)

    # Specify the desired order for "Wallpapers" sub-categories
    wallpaper_order = ['SABYASACHI', 'Versace', 'Dolce & Gabbana', 'Lamborghini', 'Good Earth', 'Philipp Plein', 'Trussardi', 'Roberto Cavalli', 'Cole & Sons', 'Tailor Weave by Burberry', 'Customization', 'Deluxe', 'Economic']

    # Conditionally order sub-categories based on the category
    sub_categories = all_sub_categories.order_by(
        Case(
            *[When(sub_cat_title=title, then=pos) for pos, title in enumerate(wallpaper_order)],
            default=Value(999),  # Default value for other sub-categories (alphabetical order)
            output_field=IntegerField()
        )
    )

    # Fetch related products using the relationships
    products = Product.objects.filter(
        category=category,
        sub_category__in=all_sub_categories,
        company_name__in=company_names
    )

    context = {
        "category": category,
        "company_names": company_names,
        "sub_categories": sub_categories,
        "products": products,
    }

    return render(request, "core/category.html", context)


def sub_category(request, sub_cat_slug):
    sub_cats = Sub_categories.objects.filter(slug=sub_cat_slug)

    if not sub_cats.exists():
        # Handle the case where no objects are found
        raise Http404("Sub-category does not exist")

    sub_cat = sub_cats.first()

    related_sub_categories = Sub_categories.objects.filter(maincat=sub_cat.maincat, category=sub_cat.category)
    company_names = Company_name.objects.filter(sub_category=sub_cat)
    
    # Create a dictionary to store company names and their associated products
    company_products = {}
    for company in company_names:
        products = Product.objects.filter(company_name=company)
        company_products[company] = products

    # Fetch sub-categories images
    sub_cat_images = SubcategoryImages.objects.filter(sub_category=sub_cat)
    image_urls = [image.images.url for image in sub_cat_images]

    context = {
        "sub_cat": sub_cat,
        "company_products": company_products,
        "related_sub_categories": related_sub_categories,
        "sub_cat_images": sub_cat_images,
        "image_urls": image_urls,
    }

    return render(request, "core/sub-category.html", context)



def main_category(request, main_slug):
    main_categories = get_object_or_404(Main_category, main_slug=main_slug)
    categories = Category.objects.filter(main_category=main_categories)

    context = {
        "main_categories": main_categories,
        "categories": categories,
    }
    return render(request, "core/main_category.html", context)

def fetch_pin_details(request):
    if request.method == 'GET':
        zipcode = request.GET.get('zipcode')
        print('Zipcode received:', zipcode)
        
        pin_details_list = indiapins.matching(zipcode)
        print('Pin details fetched:', pin_details_list)
        
        if pin_details_list:
            # Format all pin details to be sent in the response
            response_data = [
                {
                    'Name': pin_details.get('Name'),
                    'Region': pin_details.get('Region'),
                    'District': pin_details.get('District'),
                    'Division': pin_details.get('Division'),
                    'Block': pin_details.get('Block'),
                    'Circle': pin_details.get('Circle'),
                    'State': pin_details.get('State')
                }
                for pin_details in pin_details_list
            ]
            response = {
                'success': True,
                'data': response_data
            }
            print('Response:', response)  # Check if the response is correctly formatted
            return JsonResponse(response)
        else:
            return JsonResponse({'success': False, 'error': 'Pincode details not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})




def add_to_cart(request):
    # Ensure all required parameters are present
    required_params = ['id', 'title', 'qty', 'price', 'image', 'sku', 'price_wo_gst', 'gst_rate', 'gst_applied']
    for param in required_params:
        if param not in request.GET:
            return JsonResponse({"error": f"Missing parameter: {param}"}, status=400)

    product_id = request.GET.get('id')
    sku = request.GET.get('sku')
    price = request.GET.get('price')

    # Create a more unique key by including sku and price
    unique_key = f"{product_id}_{sku}_{price}" 

    try:
        qty = int(request.GET['qty'])  # Ensure qty is an integer
    except ValueError as e:
        return JsonResponse({"error": f"Invalid numeric value for qty: {str(e)}"}, status=400)

    try:
        price = Decimal(request.GET['price'])  # Ensure price is a decimal
    except InvalidOperation as e:
        return JsonResponse({"error": f"Invalid numeric value for price: {str(e)}"}, status=400)

    try:
        price_wo_gst = Decimal(request.GET['price_wo_gst'])  # Ensure price_wo_gst is a decimal
    except InvalidOperation as e:
        return JsonResponse({"error": f"Invalid numeric value for price_wo_gst: {str(e)}"}, status=400)

    try:
        gst_rate = Decimal(request.GET['gst_rate'])  # Ensure gst_rate is a decimal
    except InvalidOperation as e:
        return JsonResponse({"error": f"Invalid numeric value for gst_rate: {str(e)}"}, status=400)
    
    try:
        gst_applied = Decimal(request.GET['gst_applied'])  # Ensure gst_applied is a decimal
    except InvalidOperation as e:
        return JsonResponse({"error": f"Invalid numeric value for gst_applied: {str(e)}"}, status=400)

    cart_product = {
        'product_id': product_id,
        'title': request.GET.get('title'),
        'qty': qty,
        'price': str(price),  # Convert Decimal to string
        'image': request.GET.get('image'),
        'sku': sku,
        'price_wo_gst': str(price_wo_gst),  # Convert Decimal to string
        'gst_rate': str(gst_rate),  # Convert Decimal to string
        'gst_applied': str(gst_applied),  # Convert Decimal to string
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        # Check if the product with the same unique key is already in the cart
        if unique_key in cart_data:
            return JsonResponse({"already_in_cart": True})
        
        cart_data[unique_key] = cart_product
    else:
        cart_data = {unique_key: cart_product}

    request.session['cart_data_obj'] = cart_data

    return JsonResponse({
        "data": request.session['cart_data_obj'], 
        'totalcartitems': len(request.session['cart_data_obj']), 
        "already_in_cart": False
    })




def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        return render(request, "core/cart.html", {
            "cart_data": request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']), 
            'cart_total_amount': cart_total_amount
        })
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:main_category")



def product(request, product_slug):
    try:
        products = Product.objects.get(product_slug=product_slug)
    except Product.DoesNotExist:
        # Handle the case where no objects are found
        raise Http404("Product does not exist")

    gst_rate = products.gst_rate
    base_price = products.price
    gst_amount_applied = base_price * Decimal(gst_rate.strip('%')) / (100 + Decimal(gst_rate.strip('%')))
    price_wo_gst = base_price - gst_amount_applied
    price_wo_gst = price_wo_gst.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    gst_amount_applied = gst_amount_applied.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    related_products = Product.objects.filter(company_name=products.company_name).exclude(pk=products.pk)[:10]
    product_images = ProductImages.objects.filter(product=products)
    product_varients = ProductVarient.objects.filter(product=products)
    related_company = products.company_name
    related_subcategory = products.sub_category

    if products.product_slug:
        product_url = f"https://thepanipathandloom.com/product/{products.product_slug}/"
    else:
        product_url = f"https://thepanipathandloom.com/product/{products.title.replace(' ', '-').lower()}/"

    context = {
        "main_product": products,
        "related_products": related_products,
        "product_images": product_images,
        "related_company": related_company,
        "price_wo_gst": price_wo_gst,
        "gst_amount_applied": gst_amount_applied,
        "gst_rate": gst_rate,
        "related_subcategory": related_subcategory,
        "product_varients": product_varients,
        "ecommerce_enabled": related_company.ecommerce,  # Add this line
        "product_url": product_url,
    }
    return render(request, "core/product.html", context)

def producttitle(request, title):
    products = Product.objects.filter(title=title)

    if not products.exists():
        # Handle the case where no objects are found
        raise Http404("Product does not exist")

    # If there are multiple objects, you may want to choose one or handle the situation appropriately
    main_product = products.first()

    related_products = Product.objects.filter(company_name=main_product.company_name).exclude(pk=main_product.pk)[:10]
    product_images = ProductImages.objects.filter(product=main_product)
    product_varients = ProductVarient.objects.filter(product=main_product)
    related_company = main_product.company_name
    related_subcategory = main_product.sub_category

    if main_product.product_slug:
        product_url = f"https://thepanipathandloom.com/product/{main_product.product_slug}/"
    else:
        # Replace spaces with hyphens and convert to lowercase
        product_url = f"https://thepanipathandloom.com/product/{main_product.title.replace(' ', '-').lower()}/"

    context = {
        "main_product": main_product,
        "related_products": related_products,
        "product_images": product_images,
        "related_company": related_company,
        "related_subcategory": related_subcategory,
        "product_varients" : product_varients,
        "product_url": product_url, 
    }
    return render(request, "core/product.html", context)


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }

    return render(request, "core/search.html", context)


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    refresh_page = request.GET.get('refresh_page', False)

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
           cart_data = request.session['cart_data_obj']
           del request.session['cart_data_obj'][product_id]
           request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'refresh_page': refresh_page,  # Include refresh_page flag in context
    }

    rendered_html = render_to_string("core/cart.html", context)
    
    # Return JSON response with rendered HTML and refresh_page flag
    return JsonResponse({"data": rendered_html, 'totalcartitems': len(request.session['cart_data_obj']), 'refresh_page': refresh_page})        

def update_cart(request):
    product_id = request.GET['id']
    product_qty = request.GET['qty']
    sku = request.GET.get('sku')
    price = request.GET.get('price')
    refresh_page = request.GET.get('refresh_page', False)

    # Create the unique key using the same method as in add_to_cart
    unique_key = f"{product_id}_{sku}_{price}"

    # Print the incoming data for debugging
    print(f"Received product_id: {product_id}")
    print(f"Received qty: {product_qty}")
    print(f"Received sku: {sku}")
    print(f"Received price: {price}")
    print(f"Generated unique_key: {unique_key}")

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        
        # Check if the unique key exists in the session data
        if unique_key in cart_data:
            print(f"Found product in cart: {cart_data[unique_key]}")
            cart_data[unique_key]['qty'] = product_qty  # Update the quantity
            request.session['cart_data_obj'] = cart_data
            print(f"Updated cart data: {cart_data[unique_key]}")
        else:
            print(f"Product with key {unique_key} not found in cart")

    # Recalculate cart total amount
    cart_total_amount = 0
    for p_id, item in request.session['cart_data_obj'].items():
        cart_total_amount += int(item['qty']) * float(item['price'])
    
    # Print updated cart data for debugging
    print("Updated cart data after recalculation:")
    for p_id, item in request.session['cart_data_obj'].items():
        print(f"Product ID: {p_id}, Qty: {item['qty']}, Price: {item['price']}")

    context = render_to_string("core/cart.html", {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount
    })

    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj']), 'refresh_page': refresh_page})

 


def load_maharashtra_zipcodes():
    try:
        with open('maharashtra_zipcodes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def checkout_view(request):
    if 'cart_data_obj' not in request.session or not request.session['cart_data_obj']:
        messages.info(request, 'Please shop first before checkout')
        return redirect('/cart')
    
    cart_total_amount = Decimal('0.00')
    total_amount = Decimal('0.00')
    price_wo_gst_total = Decimal('0.00')
    total_gst = Decimal('0.00')
    user_zipcode = request.POST.get("checkout_zipcode")  # Get user's zipcode from the form

    with open('maharashtra_zipcodes.json', 'r') as f:
        maharashtra_zipcodes = json.load(f)

    # Determine GST factors based on the user's zipcode
    if user_zipcode in maharashtra_zipcodes:
        cgst_factor = Decimal('0.025')  # CGST rate for Maharashtra (2.5%)
        sgst_factor = Decimal('0.025')  # SGST rate for Maharashtra (2.5%)
        igst_factor = Decimal('0.00')   # IGST will be 0%
    else:
        cgst_factor = Decimal('0.09')   # CGST rate for other states (9%)
        sgst_factor = Decimal('0.09')   # SGST rate for other states (9%)
        igst_factor = Decimal('1.00')   # IGST will be 100%

    if 'cart_data_obj' in request.session:
        for unique_key, item in request.session['cart_data_obj'].items():
            try:
                qty = int(item['qty'])
                price_str = item['price']
                price_wo_gst_str = item.get('price_wo_gst', item['price'])

                if price_str and price_wo_gst_str:  # Check if price is not empty
                    price = Decimal(price_str)
                    price_wo_gst = Decimal(price_wo_gst_str)
                else:
                    messages.error(request, f"Price is missing for item {unique_key}")
                    return redirect('/cart')

                total_amount += qty * price
                price_wo_gst_total += qty * price_wo_gst
                item_gst = (price - price_wo_gst) * qty  # Calculate GST for this item

                # Calculate CGST, SGST, and IGST
                cgst = item_gst * cgst_factor
                sgst = item_gst * sgst_factor
                igst = item_gst * igst_factor

                total_gst += item_gst  # Add item's GST to total GST

            except ValueError as e:
                messages.error(request, f"Error processing item {unique_key}: {e}")
                return redirect('/cart')  # Redirect the user to the cart page

    # Clear previous total amount calculation before new calculations
    cart_total_amount = Decimal('0.00')

    with transaction.atomic():
        for unique_key, item in request.session['cart_data_obj'].items():
            try:
                qty = int(item['qty'])
                price_str = item['price']
                
                if price_str:  # Check if price is not empty
                    price = Decimal(price_str)
                else:
                    messages.error(request, f"Price is missing for item {unique_key}")
                    return redirect('/cart')

                cart_total_amount += qty * price
                product_id = item['product_id']
                product = Product.objects.get(pid=product_id)
                client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
                amount_in_paise = int(qty * price * 100)
                payment = client.order.create({
                    'amount': amount_in_paise,
                    'currency': 'INR',
                    'payment_capture': 1
                })
                product.razor_pay_order_id = payment['id']
                product.save()
            except ValueError as e:
                messages.error(request, f"Error processing item {unique_key}: {e}")
                return redirect('/cart')  # Redirect the user to the cart page

    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    total_amount_in_paise = int(cart_total_amount * 100)
    payment = client.order.create({
        'amount': total_amount_in_paise,
        'currency': 'INR',
        'payment_capture': 1
    })

    context = {
        "payment": payment,
        "price_wo_gst_total": price_wo_gst_total,
        "total_gst": total_gst,
        "user_zipcode": user_zipcode,
        "maharashtra_zipcodes": maharashtra_zipcodes,
    }

    return render(request, "core/checkout.html",
                  {'cart_data': request.session.get('cart_data_obj', {}),
                   'totalcartitems': len(request.session.get('cart_data_obj', {})),
                   'cart_total_amount': cart_total_amount,
                   **context})

def payment_invoice(request):
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')

    # Retrieve form data from query parameters
    query_params = request.GET
    first_name = query_params.get('first_name')
    last_name = query_params.get('last_name')
    company_name = query_params.get('company_name')
    gst_number = query_params.get('gst_number')
    zipcode = query_params.get('zipcode')
    city = query_params.get('city')
    street_address = query_params.get('street_address')
    shipping_address = query_params.get('shipping_address')
    phone = query_params.get('phone')
    email = query_params.get('email')
    checkout_district = query_params.get('checkout_district')
    checkout_division = query_params.get('checkout_division')
    checkout_state = query_params.get('checkout_state')
    shipping_street_address = query_params.get('shipping_street_address')
    shipping_address_line1 = query_params.get('shipping_address_line1')
    shipping_address_line2 = query_params.get('shipping_address_line2')
    billing_zipcode = query_params.get('billing_zipcode')
    billing_checkout_city = query_params.get('billing_checkout_city')
    billing_checkout_district = query_params.get('billing_checkout_district')
    billing_checkout_division = query_params.get('billing_checkout_division')
    billing_checkout_state = query_params.get('billing_checkout_state')
    billing_street_address = query_params.get('billing_street_address')
    billing_address_line1 = query_params.get('billing_address_line1')
    billing_address_line2 = query_params.get('billing_address_line2')
    cart_total_amount = 0
    total_amount = 0
    price_wo_gst_total = 0
    total_gst = 0

    current_datetime = datetime.now()

    with open('maharashtra_zipcodes.json', 'r') as f:
        maharashtra_zipcodes = json.load(f)

        print('payment', maharashtra_zipcodes)

    if 'cart_data_obj' in request.session:
        # Initialize dictionaries to store CGST, SGST, and IGST amounts for each product
        cgst_amounts = {}
        sgst_amounts = {}
        igst_amounts = {}
        gst_amounts = {}
        gst_amounts_combined = {}  # Dictionary to store aggregated GST amounts

        # Calculate total amount, price without GST, and total GST
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * Decimal(item['price'])
            price_wo_gst_total += int(item['qty']) * Decimal(item.get('price_wo_gst', item['price']))
            price_wo_gst_final = int(item['qty']) * Decimal(item.get('price_wo_gst', item['price']))
            item_gst = (Decimal(item['price']) - Decimal(item.get('price_wo_gst', item['price']))) * int(
                item['qty'])  # Calculate GST for this item

            # Calculate GST rates
            if price_wo_gst_final != 0:
                gst_rates_final = (item_gst / price_wo_gst_final) * 100
            else:
                gst_rates_final = Decimal('0')

            item['gst_rates_final'] = gst_rates_final

            # Divide the GST amount by 2 to get CGST and SGST separately
            if zipcode in maharashtra_zipcodes:
                # For Maharashtra zip codes, calculate CGST and SGST separately
                igst_amount = Decimal('0')  # IGST will be 0
                gst_rates_final = gst_rates_final / Decimal(2)
            else:
                # For non-Maharashtra zip codes, IGST will be double of CGST
                igst_amount = item_gst
                gst_rates_final = gst_rates_final

            # Aggregate GST amounts based on GST rates
            if gst_rates_final in gst_amounts:
                gst_amounts[gst_rates_final] += item_gst
            else:
                gst_amounts[gst_rates_final] = item_gst

            total_gst += item_gst

        # Print CGST Amounts
        print("CGST Amounts:")
        for gst_rate, total_gst_amount in gst_amounts.items():
            cgst_amount = total_gst_amount / Decimal(2)
            print(f"CGST Amount: {cgst_amount}, GST Rate: {gst_rate}")

        # Print SGST Amounts
        print("\nSGST Amounts:")
        for gst_rate, total_gst_amount in gst_amounts.items():
            sgst_amount = total_gst_amount / Decimal(2)
            print(f"SGST Amount: {sgst_amount}, GST Rate: {gst_rate}")

        print("\nIGST Amounts:")
        for gst_rate, total_gst_amount in gst_amounts.items():
            igst_amount = total_gst_amount
            print(f"IGST Amount: {igst_amount}, GST Rate: {gst_rate}")

        print("GST Amounts:")
        print(gst_amounts)

        for gst_rate, total_gst_amount in gst_amounts.items():
            cgst_amount = total_gst_amount / Decimal(2)
            sgst_amount = total_gst_amount / Decimal(2)
            gst_amounts_combined[gst_rate] = {'cgst': cgst_amount, 'sgst': sgst_amount}

        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            order = CartOrder.objects.create(
                user=request.user if request.user.is_authenticated else None,
                price=item['price'],
                firstname=first_name,
                lastname=last_name,
                zipcode=zipcode,
                order_date=current_datetime,
                pin_details=zipcode,
                city=city,
                district=checkout_district,
                division=checkout_division,
                state=checkout_state,
                shipping_street_address=shipping_street_address,
                shipping_address_line1=shipping_address_line1,
                shipping_address_line2=shipping_address_line2,
                billing_zipcode=billing_zipcode,
                billing_checkout_city=billing_checkout_city,
                billing_checkout_district=billing_checkout_district,
                billing_checkout_division=billing_checkout_division,
                billing_checkout_state=billing_checkout_state,
                billing_street_address=billing_street_address,
                billing_address_line1=billing_address_line1,
                billing_address_line2=billing_address_line2,
                phone=phone,
                email=email,
                price_wo_gst_total=price_wo_gst_total,
                
            )

            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no="order_id-" + str(order.id),
                product_status=item.get('product_status', ''),
                item=item.get('title', ''),  # Ensure this matches the field in your model
                image=item.get('image', ''),
                qty=item['qty'],
                price=item['price'],
                total=Decimal(item['qty']) * Decimal(item['price']),
                price_wo_gst=Decimal(item['price_wo_gst']),  # Store price without GST
                gst_rates_final=Decimal(item['gst_applied'])
            )

        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            with transaction.atomic():
                for unique_key, item in request.session['cart_data_obj'].items():
                    cart_total_amount += int(item['qty']) * float(item['price'])
                    product_id = item['product_id']
                    product = Product.objects.get(pid=product_id)
                    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
                    payment = client.order.create(
                        {'amount': int(item['qty']) * float(item['price']) * 100, 'currency': 'INR',
                         'payment_capture': 1})
                    product.razor_pay_order_id = payment['id']
                    product.save()

        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create({'amount': cart_total_amount * 100, 'currency': 'INR', 'payment_capture': 1})
        cart_total_amount_rounded = round(cart_total_amount, 2)
        cart_total_amount_words = num2words(cart_total_amount_rounded, lang='en_IN')

        invoice_number, created = InvoiceNumber.objects.get_or_create()

        # Increment the invoice number
        invoice_number.increment()

        # Use the incremented invoice number for the current invoice
        invoice_no = str(invoice_number)

        half_total_gst_amount = total_gst / Decimal(2)

        context = {
            "payment": payment,
            "price_wo_gst_total": price_wo_gst_total,
            "total_gst": total_gst,
            "cgst_amounts": cgst_amounts,
            "sgst_amounts": sgst_amounts,
            "igst_amounts": igst_amounts,
            "zipcode": zipcode,
            "maharashtra_zipcodes": maharashtra_zipcodes,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature,
            'first_name': first_name,
            'last_name': last_name,
            'company_name': company_name,
            'gst_number': gst_number,
            'zipcode': zipcode,
            'city': city,
            'street_address': street_address,
            'phone': phone,
            'current_datetime':current_datetime,
            'email': email,
            "cgst_amount": cgst_amount,
            "sgst_amount": sgst_amount,
            "igst_amount": igst_amount,
            "igst_amounts": igst_amounts,
            "gst_rates_final": gst_rates_final,
            "shipping_address": shipping_address,
            "cart_total_amount_words": cart_total_amount_words,
            'invoice_no': invoice_no,
            "half_total_gst_amount": half_total_gst_amount,
            "gst_amounts": gst_amounts,
            "gst_rate": gst_rate,
            "gst_amounts_combined": gst_amounts_combined,
            'cart_data': request.session.get('cart_data_obj', {}),
            'totalcartitems': len(request.session.get('cart_data_obj', {})),
            'cart_total_amount': cart_total_amount,
            'cart_items': request.session.get('cart_data_obj', {})
        }
        subject = 'Payment Invoice'
        from_email = 'princesachdeva@nationalmarketingprojects.com'
        to_email = email
        html_message = render_to_string('core/thankyou-order.html', {'context': context})
        plain_message = strip_tags(html_message)

         # Generate PDF using xhtml2pdf
        html_template = render_to_string('core/payment_invoice.html', context)
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html_template, dest=pdf_file)
        pdf_file.seek(0)

        # Create the email message
        email_message = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email_message.attach_alternative(html_message, "text/html")

        if not pisa_status.err:
            email_message.attach('invoice.pdf', pdf_file.read(), 'application/pdf')

         # Send the email
        email_message.send()

        # Render the invoice before clearing the cart data
        response = render(request, "core/payment_invoice.html", context)

        # Clear cart data after successful purchase and rendering the invoice
        if 'cart_data_obj' in request.session:
            del request.session['cart_data_obj']
            request.session.modified = True

        return response
    
def generate_invoice(request, order_id):
    # Get the order object
    order = get_object_or_404(CartOrder, pk=order_id)
    
    # Fetch related cart items
    cart_items = CartOrderItems.objects.filter(order=order)

    # Prepare data for the invoice
    cart_data = {}
    price_wo_gst_total = Decimal('0')
    for item in cart_items:
        cart_data[item.id] = {
            'title': item.item,  # Assuming 'item' is a string
            'qty': item.qty,
            'price': item.price,
            'image': item.image,
            'invoice_no': item.invoice_no,
            'product_status': item.product_status,
            'total': item.total,
            'price_wo_gst': item.price_wo_gst,  # Use the correct field name
            'gst_rates_final': item.gst_rates_final,  # Include gst_rates_final
            'first_name': order.firstname,
            'last_name': order.lastname,
            'zipcode': order.zipcode,
            'email': order.email,
            'phone': order.phone,
            'pin_details': order.pin_details,
            'city': order.city,
            'district': order.district,
            'division': order.division,
            'state': order.state,
            'shipping_street_address': order.shipping_street_address,
            'shipping_address_line1': order.shipping_address_line1,
            'shipping_address_line2': order.shipping_address_line2,
            'billing_zipcode': order.billing_zipcode,
            'billing_address_line2': order.billing_address_line2,
            'billing_checkout_city': order.billing_checkout_city,
            'billing_checkout_district': order.billing_checkout_district,
            'billing_checkout_division': order.billing_checkout_division,
            'billing_checkout_state': order.billing_checkout_state,
            'billing_street_address': order.billing_street_address,
            'billing_address_line1': order.billing_address_line1,
            'company_name': order.companyname,
            'gst_number': order.gstnumber,
        }
        price_wo_gst_total += item.price_wo_gst * item.qty
        cart_total_amount_words = num2words(price_wo_gst_total, lang='en_IN')

    context = {
        'order': order,
        'cart_data': cart_data,  # Adjust if needed
        'first_name': order.firstname,
        'last_name': order.lastname,
        'zipcode': order.zipcode,
        'email': order.email,
        'phone': order.phone,
        'pin_details': order.pin_details,
        'city': order.city,
        'district': order.district,
        'division': order.division,
        'state': order.state,
        'company_name': order.companyname,
        'gst_number': order.gstnumber,
        'shipping_street_address': order.shipping_street_address,
        'shipping_address_line1': order.shipping_address_line1,
        'shipping_address_line2': order.shipping_address_line2,
        'billing_zipcode': order.billing_zipcode,
        'billing_address_line2': order.billing_address_line2,
        'billing_checkout_city': order.billing_checkout_city,
        'billing_checkout_district': order.billing_checkout_district,
        'billing_checkout_division': order.billing_checkout_division,
        'billing_checkout_state': order.billing_checkout_state,
        'billing_street_address': order.billing_street_address,
        'billing_address_line1': order.billing_address_line1,
        'price_wo_gst_total': price_wo_gst_total,  # Add price_wo_gst_total to context
        'cart_total_amount_words': cart_total_amount_words
    }

    # Render the invoice template with the context
    return render(request, 'core/download_invoice.html', context)

def generate_invoicee(request, order_id):
    # Common logic for generating the invoice
    order = get_object_or_404(CartOrder, pk=order_id)
    cart_items = CartOrderItems.objects.filter(order=order)

    cart_data = {}
    price_wo_gst_total = Decimal('0')
    for item in cart_items:
        cart_data[item.id] = {
            'title': item.item,
            'qty': item.qty,
            'price': item.price,
            'image': item.image,
            'invoice_no': item.invoice_no,
            'product_status': item.product_status,
            'total': item.total,
            'price_wo_gst': item.price_wo_gst,
            'gst_rates_final': item.gst_rates_final,
            'first_name': order.firstname,
            'last_name': order.lastname,
            'zipcode': order.zipcode,
            'email': order.email,
            'phone': order.phone,
            'pin_details': order.pin_details,
            'city': order.city,
            'district': order.district,
            'division': order.division,
            'state': order.state,
            'shipping_street_address': order.shipping_street_address,
            'shipping_address_line1': order.shipping_address_line1,
            'shipping_address_line2': order.shipping_address_line2,
            'billing_zipcode': order.billing_zipcode,
            'billing_address_line2': order.billing_address_line2,
            'billing_checkout_city': order.billing_checkout_city,
            'billing_checkout_district': order.billing_checkout_district,
            'billing_checkout_division': order.billing_checkout_division,
            'billing_checkout_state': order.billing_checkout_state,
            'billing_street_address': order.billing_street_address,
            'billing_address_line1': order.billing_address_line1,
            'company_name': order.companyname,
            'gst_number': order.gstnumber,
        }
        price_wo_gst_total += item.price_wo_gst * item.qty
    cart_total_amount_words = num2words(price_wo_gst_total, lang='en_IN')

    context = {
        'order': order,
        'cart_data': cart_data,
        'first_name': order.firstname,
        'last_name': order.lastname,
        'zipcode': order.zipcode,
        'email': order.email,
        'phone': order.phone,
        'pin_details': order.pin_details,
        'city': order.city,
        'district': order.district,
        'division': order.division,
        'state': order.state,
        'company_name': order.companyname,
        'gst_number': order.gstnumber,
        'shipping_street_address': order.shipping_street_address,
        'shipping_address_line1': order.shipping_address_line1,
        'shipping_address_line2': order.shipping_address_line2,
        'billing_zipcode': order.billing_zipcode,
        'billing_address_line2': order.billing_address_line2,
        'billing_checkout_city': order.billing_checkout_city,
        'billing_checkout_district': order.billing_checkout_district,
        'billing_checkout_division': order.billing_checkout_division,
        'billing_checkout_state': order.billing_checkout_state,
        'billing_street_address': order.billing_street_address,
        'billing_address_line1': order.billing_address_line1,
        'price_wo_gst_total': price_wo_gst_total,
        'cart_total_amount_words': cart_total_amount_words
    }

    return render(request, 'core/download_invoice.html', context)

# New view for user invoices
def generate_user_invoice(request, order_id):
    return generate_invoicee(request, order_id)



def payment_failed_view(request):
    return render(request, "core/payment-failed.html")

def payment_invoicee(request):
    return render(request, "core/payment_invoice.html")


def com_name(request):
    return render(request, "core/sub-category.html")


def our_reviews(request):
    return render(request, "core/our_reviews.html")

def our_clients(request):
    return render(request, "core/our_clients.html")

def premium_websites(request):
    return render(request, "core/premium_websites.html")

def thankyouorder(request):
    return render(request, "core/thankyou-order.html")

def testing(request):
    return render(request, "core/old-product.html")

def our_achievements(request):
    return render(request, "core/our_achievements.html")


@login_required
def dashboard(request):
    return render(request, "core/account_dashboard.html")

@login_required
def orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    context = {
        "orders": orders
    }
    return render(request, "core/account_orders.html", context)

def order_detail(request, id):
    order = CartOrder.objects.filter(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)

    context = {
        "products": products,
    }
    return render(request, "core/order-detail.html", context)


def arch(request):
    architectures = Architecture.objects.filter(featured=True)
    architecture = Architecture.objects.filter(featured=False)
    archi = Architecture.objects.all()

    context = {
        "architectures": architectures,
        "architecture": architecture,
        "archi": archi,

    }
    return render(request, "arch/index.html", context)

def arch_name(request, name):
    architecture = get_object_or_404(Architecture, name=name)
    arch_images = ArchitectureImages.objects.filter(architecture=architecture)

    context = {
        "architecture": architecture,
        "arch_images": arch_images,
    }
    return render(request, "arch/portfolio-details.html", context)


def build(request):
    builders = Builder.objects.filter(featured=True)
    builder = Builder.objects.filter(featured=False)
    buldi = Builder.objects.all()

    context = {
        "builders": builders,
        "builder": builder,
        "buldi": buldi,

    }
    return render(request, "build/index.html", context)

def build_name(request, name):
    builder = get_object_or_404(Builder, name=name)
    build_images = BuilderImages.objects.filter(builder=builder)

    context = {
        "builder": builder,
        "build_images": build_images,
    }
    return render(request, "build/portfolio-details.html", context)



def about(request):
    return render(request, "core/about-us.html")

def contact(request):
    return render(request, "core/contact-us.html")

def career(request):
    return render(request, "core/career.html")

def download_invoice(request):
    return render(request, "core/download_invoice.html")

def write_to_ceo(request):
    return render(request, "core/write-to-ceo.html")

def blogs(request):
    blogs = Blogs.objects.all()

    context = {
        "blogs": blogs,
    }
    return render(request, "core/blog.html",  context)

def blog_details(request, blog_slug):
    blog_detail = Blogs.objects.get(blog_slug=blog_slug)

    context = {
        "blog_detail": blog_detail,
    }

    return render(request, "core/blog-details.html", context)

def privacypolicy(request):
    privacy_policy = PrivacyPolicy.objects.first()  # Assuming you have a PrivacyPolicy instance
    context = {
        'privacy_policy_content': privacy_policy.privacy_policy_content if privacy_policy else ''
    }
    return render(request, 'core/privacy-policy.html', context)

class RobotsTxtView(View):
    def get(self, request, *args, **kwargs):
        # Specify the path to your robots.txt file
        robots_txt_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')

        with open(robots_txt_path, 'r') as f:
            content = f.read()

        return HttpResponse(content, content_type='text/plain')

def our_works(request):
    works = Works.objects.filter(status="published").order_by('order')
    works_images = WorksImages.objects.filter(works__in=works)

    return render(request, "core/our_works.html", {'works': works, 'works_images': works_images})

def our_media(request):
    media = Media.objects.filter(status="published")

    context = {
        "media":media,

    }
    return render(request, "core/our_media.html", context)




        
    





