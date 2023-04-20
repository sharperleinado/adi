from asyncio.windows_events import NULL
from tkinter.tix import FileEntry
from django.shortcuts import render,redirect
from food_app.models import Food,Soup

# Create your views here.


def search_box(request):

    if request.method == "POST":
        search_box = request.POST.get("search").strip()
        food_box = Food.objects.filter(food_item__contains = search_box).all()
        soup_box = Soup.objects.filter(soup_item__contains = search_box).all()
        search_list = [search_box,food_box,soup_box]

        return render(request,'search_box/search.html',{'searched':search_box,'food':food_box,'soup':soup_box,
        'search_list':search_list})
    
