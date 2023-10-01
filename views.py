
import re
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.apps import apps
#from .models import Feedback
from django.views.generic import CreateView
#from .form import ContactForm
Product=apps.get_model('accounts','Product')
Category=apps.get_model('accounts','Category')


def Indexpage(request):
    return render(request,'index.html')

def login(request):
    return render(request,'index.html')    


def logout(request):
    try:
        del request.session['user_email']
    except:
        return render(request,'index.html')
    return render(request,'index.html')


def menu(request):
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
    return render(request,'menu.html',data)

#class contact_us(CreateView):
#    model = Feedback
#    form_class = ContactForm
#    template_name = 'contact.html'

 #   def form_valid(self, form):
  #      user = form.save()
   #     contact_us(self.request)
    #    return redirect('/')
    

def About(request):
    return render(request,'about.html')

def icons(request):
    return render(request,'icons.html')

def codes(request):
    return render(request,'codes.html')

def contact(request):
    return render(request,'contact.html')

def careers(request):
    return render(request,'careers.html')    

def pwu(request):
    return render(request,'help.html')

def faq(request):
    return render(request,'faq.html')

def offers(request):
    return render(request,'offers.html')

def privacy(request):
    return render(request,'privacy.html')

def terms(request):
    return render(request,'terms.html')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})