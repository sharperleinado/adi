from django.urls import path
from . import views



app_name = 'payments'



urlpatterns = [
    path('<int:price><slug:slug>/',views.payment,name='payment'), #This is for payment page
    path('<slug:slug>/',views.price_in_pack,name='price'), #This is for price in pack page
    path('payment_api/',views.payment_api,name='payment_api'), #This is going to be for paystack
]

