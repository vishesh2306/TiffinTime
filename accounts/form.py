from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Customer,Employee,Feedback,Weekly_menu,Product

class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number=self.cleaned_data.get('phone_number')
        customer.save()
        return user

class EmployeeSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user)
        employee.phone_number=self.cleaned_data.get('phone_number')
        employee.save()
        return user

class ContactForm(forms.ModelForm):
    class Meta():
        model = Feedback  
        fields=('name','email','phone_number','messege')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name')
        user.email=self.cleaned_data.get('email')
        user.phone_number=self.cleaned_data.get('phone_number')
        user.messege=self.cleaned_data.get('messege')
        user.save()
        return user

class MenuForm(forms.ModelForm):
    class Meta():
        model = Product
        fields=('name','category','description','price','image')

    @transaction.atomic
    def save(self,staff):
        user = super().save(commit=False)
        emp=Employee.objects.get(user_id=staff)
        user.employee=emp
        user.save()
        return user

class WeeklyForm(forms.ModelForm):
    class Meta():
        model = Weekly_menu
        fields=('category','monday','tuesday','wednesday','thursday','friday','saturday','sunday')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user

    