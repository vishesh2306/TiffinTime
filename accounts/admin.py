from django.contrib import admin
from .models import User, Customer, Employee, Product,Category,Validity_pack,Feedback, NotificationStaffs,FeedBackStaffs

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(NotificationStaffs)
admin.site.register(FeedBackStaffs)

class AdminProduct(admin.ModelAdmin):
    list_display=['id','name','price','category']
    list_filter=['id','name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display=['id','name']
    list_filter=['id','name']

class AdminPack(admin.ModelAdmin):
    list_display=['id','name','price']
    list_filter=['id','name','price']

class AdminFeedback(admin.ModelAdmin):
    list_display=['id','name','phone_number','email','messege','created_on']
    list_filter=['id','email','created_on']

admin.site.register(Product, AdminProduct)
admin.site.register(Feedback, AdminFeedback)
admin.site.register(Validity_pack, AdminPack)
admin.site.register(Category,AdminCategory)