from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import AddressForm,UpdateForm
from .models import UserAddress
from django.contrib import messages


# Create your views here.


def register_address(request):
    instance = ""
    try:
        form = AddressForm()
        if request.method == "POST":
            form = AddressForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                try:
                    if UserAddress.objects.get(user=instance.user):
                        messages.error(request, "You have already created address, you can go ahead to Update or Edit your address.")
                        return redirect('address:billing_address')
                except:
                    pass
                instance.save()
                messages.success(request, "You have successfully added a shipping address!")
                messages.success(request, "You can proceed to order a meal now!")
                return redirect('home')
    except:
        pass
    
    return render(request,'address/register_address.html',{'form':form})



def billing_address(request):
    user = ""
    try:
        user = UserAddress.objects.get(user=request.user)
    except AttributeError:
        messages.error(request, "Please, create address before viewing Home page!")
        return redirect('address:register_address')
    except:
        messages.error(request, "Please, create address before viewing Home page!")
        return redirect('address:register_address')

    return render(request,'address/billing_address.html',{'form':user})



def update_address(request):
    form = UpdateForm()
    try:
        user = UserAddress.objects.get(user=request.user)
    except:
        messages.error(request, "Please, create address before updating address!")
        return redirect('address:register_address') 
    try:
        if request.method == "POST":
            form = UpdateForm(request.POST)
            if form.is_valid():
                address = UserAddress.objects.get(user=request.user)
                address.user = request.user
                address.country = form.cleaned_data["country"]
                address.state = form.cleaned_data["state"]
                address.area = form.cleaned_data["area"]
                address.city = form.cleaned_data["city"]
                address.street_name = form.cleaned_data["street_name"]
                address.save()
                messages.error(request, "You have successfully updated address.")
                return redirect('address:billing_address')
    except:
        pass
    
    return render(request,'address/update_address.html',{'form':form})

