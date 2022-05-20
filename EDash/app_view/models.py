from itertools import product
from operator import mod
from tkinter import Widget
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Catagory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.name
    
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=255)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    desc = models.TextField()
    qty = models.IntegerField(default=0)
    m_price = models.IntegerField(default=0)
    retail = models.IntegerField(default=0)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    

class Cart(models.Model):
    customer = models.CharField(max_length=255)
    phone_no = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.customer
    
class CashMemo(models.Model):
    name=models.CharField(max_length=255)
    cart_no = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    
class Order(models.Model):
    cart_no = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cash_memo = models.ForeignKey(CashMemo, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    
    
class Restriction(models.Model):
    name = models.CharField(max_length=255)
    value = models.BooleanField(default=False)