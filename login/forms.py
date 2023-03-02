from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm#this django form fields tha django creates automatically for us
from django.contrib.auth.models import User
from django.forms import fields#this is the model table for the users which django creates automatically for us
from .models import *


class AddUserDetailsForm(forms.ModelForm): #the forms here is the one imported up there.
    class Meta:
        model = UserDetailsModel
        fields = ["username",'password']

class CreateUserForm(UserCreationForm):
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
   
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2','is_superuser']#all these fields are from django


class UserEditForm(UserChangeForm):
    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    last_login=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    is_superuser=forms.CharField(max_length=50,widget=forms.CheckboxInput(attrs={"class":"form-check"}))
    is_staff=forms.CharField(max_length=50,widget=forms.CheckboxInput(attrs={"class":"form-check"}))
    is_active=forms.CharField(max_length=50,widget=forms.CheckboxInput(attrs={"class":"form-check"}))
    date_joined=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
   
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','last_login','is_superuser','is_staff','is_active','date_joined']#all these fields are from django


