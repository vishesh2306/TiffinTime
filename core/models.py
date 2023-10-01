from django.conf import settings
from django.db import models
from accounts.models import Product,Employee
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils import timezone
from datetime import timedelta
import datetime

class Time_val(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def get_all_categories():
        return Time_val.objects.all()
    
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    vender = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    duration=models.ForeignKey(Time_val, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        price=0
        if self.duration.id==1:
            return self.quantity * self.item.price * 7
        elif self.duration.id==2:
            return self.quantity * self.item.price * 28
        elif self.duration.id==3:
            return self.quantity * self.item.price * 85
        else:
            return self.quantity * self.item.price * 7

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        d=self.get_duration()
        print(d)
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()
    def get_duration(self):
        return self.duration

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if total < 1000 and total > 0:
                total +=50
        return total

    def get_all_items(self):
        name=''
        qty=''
        vender=''
        desc=''
        id=''
        for item in self.items.all():
                name=name+str(item.item.id)+' '+str(item.item.name)+' '+str(item.quantity)+' '+str(item.vender)+','
                qty=qty+str(item.quantity)+','
                vender=vender+str(item.vender)+','
                desc=desc+str(item.item.name)+','
                id=id+str(item.item.id)+','
        return {'name':name[:-1],'qty':qty[:-1],'vender':vender[:-1],'id':id[:-1],'desc':desc[:-1]}


class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

     