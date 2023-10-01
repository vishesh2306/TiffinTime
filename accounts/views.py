from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import tree
from django.views.generic import CreateView
from django.core.mail import send_mail, BadHeaderError
from .form import CustomerSignUpForm, EmployeeSignUpForm, ContactForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, User, Feedback, Employee

def index(request):
    return render(request, 'index.html')

class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        
        return redirect('/accounts/login')

class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'employee_register.html'

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('/accounts/login1')

class contact(CreateView):
    model = Feedback
    form_class = ContactForm
    template_name = 'contact.html'
    
    def form_valid(self, form):
        user = form.save()
        return redirect('/')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(User.is_customer==True,username=username, password=password)
            print(user.is_staff)
            if user is not None and user.is_staff==False:
                login(request,user)
                return redirect('/accounts/customer_home')#customer
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'login1.html',
    context={'form':AuthenticationForm()})
#vender login
def login_request1(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user.is_staff)
            if user is not None and user.is_staff==True:
                login(request,user)
                return redirect('/accounts/staff_home')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
               
    return render(request, 'login.html',
    context={'form':AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')

def Testurl(request):
    return HttpResponse("Ok")