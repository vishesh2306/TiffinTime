import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User as CustomUser,Customer,FeedBackCustomers,NotificationCustomers
from core.models import Order,CheckoutAddress,OrderItem
from django.apps import apps
Product=apps.get_model('accounts','Product')
Category=apps.get_model('accounts','Category')

#from student_management_app.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, \
 #   LeaveReportStudent, FeedBackStudent, NotificationStudent, StudentResult, OnlineClassRoom, SessionYearModel

def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

def customer_home(request):
   # student_obj=Students.objects.get(admin=request.user.id)
   # attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
   # attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    #attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
   # course=Courses.objects.get(id=student_obj.course_id.id)
   # subjects=Subjects.objects.filter(course_id=course).count()
   # subjects_data=Subjects.objects.filter(course_id=course)
   # session_obj=SessionYearModel.object.get(id=student_obj.session_year_id.id)
   # class_room=OnlineClassRoom.objects.filter(subject__in=subjects_data,is_active=True,session_years=session_obj)

    subject_name=[]
    data_present=[]
    data_absent=[]
  #  subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
   # for subject in subject_data:
    #    attendance=Attendance.objects.filter(subject_id=subject.id)
     #   attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
      #  attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
       # subject_name.append(subject.subject_name)
     #   data_present.append(attendance_present_count)
      #  data_absent.append(attendance_absent_count)

    products=Product.get_all_products();
    categorys=Category.get_all_categories();
    CategoryId=request.GET.get('category')
    if CategoryId:
        products=Product.get_all_products_by_categoryid(CategoryId);
    else:
        products=Product.get_all_products();
    print(products)
    data={}
    data['products']=products
    data['categorys'] = categorys   
    return render(request,"customer_template/customer_home_template.html",data)


def customer_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(user_id=user)
    return render(request,"customer_template/customer_profile.html",{"user":user,"customer":customer})

def customer_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("customer_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
                customuser.save()
                messages.success(request, "Successfully Updated Profile")
                return HttpResponseRedirect(reverse("login"))
            customuser.save()

            customer=Customer.objects.get(user=customuser.id)
            customer.address=address
            customer.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("customer_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("customer_profile"))

def customer_feedback(request):
    customer_id=Customer.objects.get(user_id=request.user.id)
    feedback_data=FeedBackCustomers.objects.filter(customer_id=customer_id)
    return render(request,"customer_template/customer_feedback.html",{"feedback_data":feedback_data})

def customer_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("customer_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        customer_obj=Customer.objects.get(user_id=request.user.id)
        try:
            feedback=FeedBackCustomers(customer_id=customer_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("customer_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("customer_feedback"))

def customer_all_notification(request):
    customer=Customer.objects.get(user_id=request.user.id)
    notifications=NotificationCustomers.objects.filter(customer_id=customer)
    return render(request,"customer_template/all_notification.html",{"notifications":notifications})


@csrf_exempt
def student_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        student=Customer.objects.get(admin=request.user.id)
        student.fcm_token=token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def customer_order_history(request):
    order= Order.objects.filter(ordered=True,user_id=request.user.id)
    return render(request,"customer_template/order-history.html",{'order':order})


def customer_order_information(request):
    Id=request.GET.get('order_id')
    order= Order.objects.get(id=Id)
    amt=order.payment.amount
    if amt-50 < 1000:
        deli=50
    else:
        deli=0
    items=OrderItem.objects.filter(order=order.id)
    user=CustomUser.objects.get(id=order.user.id)
    address=CheckoutAddress.objects.get(user_id=user.id,id=order.checkout_address_id)
    return render(request,"customer_template/order-information.html",{'order':order,'user':user,'address':address,'items':items,'deli':deli})