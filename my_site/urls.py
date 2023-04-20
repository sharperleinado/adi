from django.contrib import admin
from django.urls import path,include 
from django.shortcuts import render
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from cart.models import CartItemsFood,Cart



def home(request):
    fname = ""
    cart = ""
    items_in_cart = ""
    length =""
    
    try:
        fname = request.user.first_name
        cart = Cart.objects.get(user=request.user)
        items_in_cart = CartItemsFood.objects.filter(cart=cart)
        length = len(items_in_cart)

    except:
        pass

    return render(request,'home.html',{'fname':fname,'len':length,'cart':cart})


def profile(request):
    fname=""
    try:
        fname = request.user.first_name
    except:
        pass

    return render(request,'profile.html',{'fname':fname})

     
urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/',include('authentication.urls')),
    path('food_app/',include('food_app.urls')),
    path('',home,name='home'),
    path('search/',include('search_box.urls')),
    path('payments/',include('payments.urls')),
    path('profile/',profile,name='profile'),
    path('address/',include('address.urls')),
    path('review/',include('review.urls')),
    path('cart/',include('cart.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
