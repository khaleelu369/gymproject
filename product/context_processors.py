from .models import category,Cart,CartItem
from .views import _cart_id


def menu_links(request):
    links = category.objects.all()
    return dict(links=links)


def counter(request):
    cart_count =0
    if 'admin'in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            cart_items=CartItem.objects.all().filter(cart=cart[:1])
            for car_item in cart_items:
                cart_count += car_item.quantity
        except cart.DoesNotExist:
            cart_count =0
    return dict(cart_count=cart_count)
            