from django.http import Http404
from django.shortcuts import redirect,render
from food_app.models import Food, Soup
from payments.forms import PaymentForm
from cart.models import Cart,CartItemsFood,CartItemsSoup
from django.contrib import messages
from django.http import JsonResponse,HttpResponse


# Create your views here.

#what food box function does is, first, I used a for loop on the model Food, then listed all the field in the models
#such as: image,food_item,food_price and food slug. put the=m in a list
#and then append them into a list and did the same for all the objects in the model.

def food_box_func():
    my_food_box = Food.objects.all()

    append_list_item = []
    for item in my_food_box:
        image = item.image
        food_item = item.food_item
        food_price = int(item.food_price)
        food_slug = item.slug
        list_item = [image,food_item,food_price,food_slug]
        new_list_item = append_list_item.append(list_item)
    return append_list_item


def soup_box_func():
    my_soup_box = Soup.objects.all()

    append_list_item2 = []
    for item in my_soup_box:
        image = item.image
        soup_item = item.soup_item
        mini = int(item.mini_box)
        medium = int(item.medium_box)
        mega = int(item.mega_box)
        slug = item.slug
        list_item2 = [image,soup_item,mini,medium,mega,slug]
        new_list_item2 = append_list_item2.append(list_item2)
    return append_list_item2



def food_box(request):
    cart = ""
    cart_items = "" 
    caritems_food = ""
    caritems_soup = ""
    latest = ""
    if request.method == "POST":
        add_item = request.POST.get("add-item")
        if add_item:
            cart = Cart.objects.get_or_create(user=request.user,is_paid=False,total_price=0)
                        
            food = Food.objects.get(slug=add_item)
            
            cart_user = Cart.objects.get(user=request.user)
            cartitems = CartItemsFood.objects.get_or_create(cart=cart_user,product=food)
            latest_item = CartItemsFood.objects.latest('id')
            latest = latest_item.product.food_item
            latest_price = latest_item.product.food_price
            messages.error(request, f"You have added {latest.capitalize()}, price: {latest_price} to cart!")
            return redirect('food_app:foodbox')
            
    return render(request,'food_app/food_box.html',{'item':food_box_func()})    


def soup_box(request):
    
    return render(request,'food_app/soup_box.html',{'item2':soup_box_func()})


#Food_search renders all the food and soup search on a different template and accepts a slug request when sent from the user
#which filters the provided slug in the model and display the object model searched by the user to the user.
def food_search(request,slug):
    my_food_box = ""
    my_soup_box = ""
    price = 11
    
    try:
        my_food_box = Food.objects.get(slug=slug)
    except:
        pass

    try:
        my_soup_box = Soup.objects.get(slug=slug)
    except:
        pass

    return render(request,'food_app/food_search.html',{'price':price,'item':my_food_box,'item2':my_soup_box}) 


def add_to_cart(request):

    return JsonResponse("It is working", safe=False)



