from django import forms
from .models import UserAddress
from .models import country_choice,state,city,area

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ["country","state","city","area","street_name"]


class UpdateForm(forms.Form):
    country = forms.ChoiceField(choices=country_choice, required=True)
    state = forms.ChoiceField(choices=state, required=True)
    city = forms.ChoiceField(choices=city, required=True)
    area = forms.ChoiceField(choices=area, required=True)
    street_name = forms.CharField(max_length=200, required=True)

