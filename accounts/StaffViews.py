import json
from datetime import datetime
from time import timezone
from uuid import uuid4
from datetime import date
from django.views.generic import CreateView
from django.db.models.fields import DurationField
from .models import User as CustomUser,Employee, Validity_pack, FeedBackStaffs, NotificationStaffs,Weekly_menu
from core.models import Order,OrderItem,Product
from django.contrib import messages
from .form import MenuForm,WeeklyForm
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def staff_home(request):
    products=Product.objects.filter(employee_id=request.user.id).count()
    notifications=NotificationStaffs.objects.filter(staff_id=request.user.id).count()
    staff=Employee.objects.get(user_id=request.user.id)
    product=Product.objects.filter(employee_id=request.user.id)
    prod=[]
    order= Order.objects.filter(ordered=True).count()
    feedbacks=FeedBackStaffs.objects.filter(staff_id=request.user.id).count()

    #Fetch Attendance Data by Subject
    order_list=[]
    product_list=[]
    for prod in product:
        order_list.append(prod.name)

    context={"product_count":products,"order_count":order,"notification_count":notifications,"feedback_count":feedbacks}
    return render(request,"staff_template/staff_home_template.html",context)

    
def staff_profile(request):
    print(request.user.id)
    user1=CustomUser.objects.get(id=request.user.id)
    staff=Employee.objects.get(user=user1)
    return render(request,"staff_template/staff_profile.html",{"user":user1,"staff":staff})


def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
                customuser.save()
                messages.success(request, "Successfully Updated Profile")
                return HttpResponseRedirect(reverse("login1"))
            customuser.save()

            staff=Employee.objects.get(user=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))



def staff_account(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=Employee.objects.get(user=customuser)
    packs=Validity_pack.objects.all()
    return render(request,"staff_template/staff_account.html",{"user":customuser,"staff":staff,"packs":packs})


def staff_account_save(request):
     if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_account"))
     else:
        license=request.POST.get("license")
        Validity=request.POST.get("Validity")
        try:
            user=CustomUser.objects.get(id=request.user.id)
            user.save()
            print(user.id)
            staff=Employee.objects.get(user_id=user.id)
            staff.license=license
            print(license)
            staff.acc_id=Validity
            print(Validity)
            staff.save()
            messages.success(request, "Successfully Updated Account")
            print("yayy")
            return HttpResponseRedirect(reverse("staff_account"))
        except:
            messages.error(request, "Failed to Update Account")
            print("nayyy")
            return HttpResponseRedirect(reverse("staff_account"))

def staff_feedback(request):
    staff_id=Employee.objects.get(user_id=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Employee.objects.get(user_id=request.user.id)
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def staff_all_notification(request):
    staff=Employee.objects.get(user_id=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff)
    return render(request,"staff_template/all_notification.html",{"notifications":notifications})

def view_orders(request):
    staff=Employee.objects.get(user_id=request.user.id)
    product=Product.objects.filter(employee_id=staff.user_id)
    prod=[]
    order= Order.objects.filter(ordered=True)
    return render(request,"staff_template/view_orders.html",{'order':order,'product':product})

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Employee.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")



def save_student_result(request):
    if request.method!='POST':
        return HttpResponseRedirect('staff_add_result')
    student_admin_id=request.POST.get('student_list')
    assignment_marks=request.POST.get('assignment_marks')
    exam_marks=request.POST.get('exam_marks')
    subject_id=request.POST.get('subject')


    #student_obj=Students.objects.get(admin=student_admin_id)
    #subject_obj=Subjects.objects.get(id=subject_id)

def staff_menu(request):
    staff_id=Employee.objects.get(user_id=request.user.id)
    menu_data=Product.objects.filter(employee=staff_id)
    return render(request,"staff_template/my_menu.html",{"menu_data":menu_data})

def my_menu(request):
    staff=Employee.objects.get(user_id=request.user.id)
    menu_data=Product.objects.filter(employee=staff)
    form=MenuForm()
    submit="Save"
    context={
       "form":form,
        "submit":submit,
        "menu_data":menu_data
    }
    if request.method=='POST':
        form=MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user.id)
            messages.success(request, "Your Product has been updated")
            return redirect('my_menu')
        else:
            form=MenuForm()
    return render(request, "staff_template/my_menu.html",context)

def staff_weekly_menu(request):
    staff=Employee.objects.get(user_id=request.user.id)
    print(staff)
    menu_data=Product.objects.filter(employee_id=staff.user_id)
    print(menu_data)
    for obj in menu_data:
        weekly_data=Weekly_menu.objects.filter(category=obj.id)
    print(weekly_data)
    form=WeeklyForm()
    form.fields["category"].queryset=Product.objects.filter(employee_id=staff.user_id)
    submit="Save"
    context={
       "form":form,
        "submit":submit,
        "weekly_data":weekly_data
    }
    if request.method=='POST':
        form=WeeklyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Menu has been added")
            return redirect('staff_weekly_menu')
        else:
            form=MenuForm()
    return render(request, "staff_template/staff_weekly_menu.html",context)
   

def returnHtmlWidget(request):
    return render(request,"widget.html")