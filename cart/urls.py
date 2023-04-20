from django.urls import path 
from .import views 



app_name = 'cart'



urlpatterns = [
    #path('<str:cart>/<slug:slug>/',views.cart_items,name='cart_items'),
    path('',views.cart_items,name='cart_items'),
]
