from django import forms 
from .models import Mobile
from phonenumber_field.modelfields import PhoneNumberField

#This form is for creating a phone number.
class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = ['phone_no']


#This form is for updating existing phone number.   
class UpdateMobileForm(forms.Form):
    phone_no = forms.CharField(required=True)


class EmailReset(forms.Form):
    email = forms.CharField(required=True, label="E-mail or Username",max_length=100,widget=forms.TextInput(attrs={'placeholder':"Please, enter your email or username"}))

