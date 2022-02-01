from atexit import register
from itertools import product
from django import template
from mainApp.models import Product
register = template.Library()

@register.filter(name="cartQuantity")
def cartQuantity(request,pid):
    cart = request.session.get('cart',None)
    if(cart):
        for key,value in cart.items():
            if(str(pid)==key):
                return value
    return 0

@register.filter(name="cartTotal")
def cartTotal(request,pid):
    cart = request.session.get('cart',None)
    p = Product.objects.get(pid=pid)
    if(cart):
        for key,value in cart.items():
            if(str(pid)==key):
                return value*p.finalPrice
    return 0