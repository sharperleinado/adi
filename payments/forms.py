from django import forms 


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(required=False)
    card_num = forms.CharField(max_length=20,required=True)
    expiry_month = forms.CharField(max_length=2,required=True)
    expiry_year = forms.CharField(max_length=4,required=True)
    cvv = forms.CharField(max_length=4, required=True)
