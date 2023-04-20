from django.contrib import admin
from .models import Cart
from cart.models import CartItemsFood,CartItemsSoup

# Register your models here.



admin.site.register(Cart)
admin.site.register(CartItemsFood)
admin.site.register(CartItemsSoup)
