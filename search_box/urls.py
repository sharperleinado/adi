from django import views
from django.urls import path
from . import views 


app_name = 'search_box'



urlpatterns = [
    path('',views.search_box,name='search')
]