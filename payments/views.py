from django.shortcuts import render
from food_app.models import Food, Soup
from food_app.views import food_box_func,soup_box_func
from .forms import PaymentForm
# Create your views here.


#What I did here is that I called the food and soup model function, then I looped through the items,
#Set an if-statement condition so that once the price and slug request == any of the particular request item, 
# it returns the item objects in the front end  
def payment(request, price, slug):
    payment_form = PaymentForm()
    item = ""
    item2 = ""    
    try:
        for item in food_box_func():
            if price == item[2] and slug == item[3]:
                break
    except:
        pass

    try:
        for item2 in soup_box_func():
            if price == item2[2] and slug == item2[5] or price == item2[3] and slug == item2[5] or price == item2[4] and slug == item2[5] or price == 11 and slug == item2[5]:
                break
    except:
        pass
    
    return render(request,'payments/pay.html',{'price':price,'slug':slug,'item':item,'item2':item2,'form':payment_form})


#What I did here is, I first got the price_in_pack input from the user,
#Then if the slug request taken from the price_in_pack form is equal to the slug in the price_in_pack, the program breaks out of the loop and return the view to the user 
def price_in_pack(request, slug):
    total_price = ""
    quantity = ""
    if request.method == "POST":
            try:
                quantity = int(request.POST.get("quantity"))
                for item in food_box_func():
                    if slug == item[3]:
                        break
                total_price = quantity*item[2]
            except ValueError:
                return render(request,'food_app/404.html')

    return render(request,'payments/price.html',{'form':PaymentForm(),'slug':slug,'quantity':quantity,'total_price':total_price,'item':item})


def payment_api(request):

    return render(request,'payments/payment_api.html')

    