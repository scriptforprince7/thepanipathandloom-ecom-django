from core.models import *

def default(request):
    product = Main_category.objects.all()

    return {
        'main_cat': product,
    }

def defaultOne(request):
    architectures = Architecture.objects.filter(featured=True)
    architecture = Architecture.objects.filter(featured=False)
    archi = Architecture.objects.all()

    return {
        "architectures": architectures,
        "architecture": architecture,
        "archi": archi,
    }

def defaultTwo(request):
    walpaper_cat = Company_name.objects.filter(wallpaper_category=True)

    return {
        "walpaper_cat": walpaper_cat,
    }

def cart_context(request):
    cart_total_amount = 0
    total_cart_items = 0
    cart_data = {}

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        for p_id, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total_cart_items += int(item['qty'])

    return {
        'cart_total_amount': cart_total_amount,
        'total_cart_items': total_cart_items,
        'cart_data': cart_data  # Include cart_data in the context
    }