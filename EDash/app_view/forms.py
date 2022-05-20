from dataclasses import field
from tkinter import Widget
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User


from django.forms import ModelForm, TextInput, Select, NumberInput, EmailInput, PasswordInput
from .models import Cart, CashMemo, Product, Catagory

class ProductForm(ModelForm):
    class Meta:
        classes = {"class": "col-12", "style": "height:45px;margin: 5px 0px"}
        model = Product
        fields = '__all__'
        widgets = {
            "name": TextInput(attrs=classes),
            "catagory": Select(attrs=classes),
            "desc": Textarea(attrs=classes),
            "qty": NumberInput(attrs=classes),
            "m_price": NumberInput(attrs=classes),
            "retail": NumberInput(attrs=classes),
            
        }
        
class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = "__all__"
        
class CatagoryForm(ModelForm):
    class Meta:
        model = Catagory
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"class": "col-12", "style": "height:40px;margin: 5px 0px"}),
        }

class MemoForm(ModelForm):
    class Meta:
        model = CashMemo
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"class": "col-md-4 col-10", "style": "height:40px;margin: 5px 0px"}),
            "cart_no": Select(attrs={"class": "col-md-4 col-10", "style": "height:40px;margin: 5px 0px"}), 
        }
class UserForm(ModelForm):
    class Meta:
        classes = {"class": "col-9"}
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        widgets = {
            "first_name": TextInput(attrs=classes),
            "last_name": TextInput(attrs=classes),
            "email": EmailInput(attrs=classes),
            "username": TextInput(attrs=classes),
            "password": PasswordInput(attrs=classes),
        }