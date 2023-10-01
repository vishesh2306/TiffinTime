from django.contrib import admin
from accounts.models import Product
from .models import (
    
    OrderItem, 
    Order,
    CheckoutAddress,
    Payment,
    Time_val
)

#admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CheckoutAddress)
admin.site.register(Payment)
admin.site.register(Time_val)
