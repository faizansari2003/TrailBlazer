from django import forms
from .models import Customer,Address
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django import forms
from django.contrib.auth.models import User





class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password'] 
        field_order = ['first_name','last_name','username','email','password','confirm_password'] # add other necessary fields here
        widgets = {
            'dob': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_dob'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

from django import forms
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']



# forms.py
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'address_line_1', 'address_line_2', 'pincode', 'city','state']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Home, Work', 'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Enter address line 1', 'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Enter address line 2', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city', 'class': 'form-control'}),
            'pincode': forms.NumberInput(attrs={'placeholder': 'Enter pincode', 'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
        }



class ForgetPasswordForm(forms.Form):
    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'h-12 w-60 sm:w-80 rounded-md'}))
    email = forms.CharField(max_length=50,widget=forms.EmailInput(attrs={'placeholder':'Enter email','class':'h-12 w-60 sm:w-80 rounded-md'}))




class OTPForm(forms.Form):
    otp = forms.IntegerField(max_value=9999,min_value=1000,widget=forms.NumberInput(attrs={'placeholder':'Enter 4-digit otp','class':'w-60 sm:w-80 rounded-md'}))




class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter new password','class':'w-60 sm:w-80 rounded-md'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm new password','class':'w-60 sm:w-80 rounded-md'}))