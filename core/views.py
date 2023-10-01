from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm
from django.apps import apps
Product=apps.get_model('accounts','Product')
Category=apps.get_model('accounts','Category')
Employee=apps.get_model('accounts','Employee')
Weekly_menu=apps.get_model('accounts','Weekly_menu')
from .models import (

    Order,
    OrderItem,
    CheckoutAddress,
    Payment,
    Time_val
)

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
#class HomeView(ListView):
#    model = Item
#    template_name = "menu.html"

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


class ProductView(DetailView):
    model = Product
    template_name = "product.html"
   

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            duration=Time_val.objects.all()
            context = {
                'object': order,
                'duration':duration
            }
            return render(self.request, 'customer_template/order_summary.html', context)
        except ObjectDoesNotExist:
            msg=messages.error(self.request, "You do not have an order")
            return render(self.request,'customer_template/order_summary.html',msg)

        
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'checkout.html', context)


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionaly for these fields
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid Payment option")
                    return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("core:order-summary")

class OrderSuccess(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        
        context = {
            'order': order
        }
        return render(self.request, 'order_success.html', context)


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "payment.html", context)
    
    def post(self, *args, **kwargs):  
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = 'tok_visa'
        print(token)
        amount = int(order.get_total_price()*100)  #cent
        try:
            charge = stripe.Charge.create(
                source=token,
                amount=amount,
                currency="inr",
                
            )
            print(token)

            # create payment
            payment = Payment()
            payment.stripe_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_price()
            payment.save()

            # assi gn payment to order
            order.ordered = True
            order.payment = payment
            order.save()
            data=order
            amt=order.payment.amount
            if amt-50 < 1000:
                deli=50
            else:
                deli=0
            items=OrderItem.objects.filter(order=order.id)
            return redirect('core:order_success',{'order':data,'items':items,'deli':deli})

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('core:checkout')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "To many request error")
            return redirect('core:checkout')

        except stripe.error.InvalidRequestError as e:
            print(e)
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid Parameter")
            return redirect('core:checkout')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Authentication with stripe failed")
            return redirect('core:checkout')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect('core:checkout')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect('core:checkout')
        
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "Not identified error")
            return redirect('core:checkout')
            #data=order
            #amt=order.payment.amount
            #if amt-50 < 1000:
            #    deli=50
            #else:
            #    deli=0
            #items=OrderItem.objects.filter(order=order.id)
            #return render(self.request, "order_success.html",{'order':data,'items':items,'deli':deli})
            #messages.success(self.request, "Order Successful")
            

@login_required        
def update_duration(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            time=Time_val.objects.get(id=request.POST['dropdown'])
            order_item.duration=time
            print(request.POST['dropdown'])
            order_item.save()
            messages.info(request, "Duration is updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Not Found")
            return redirect("core:order-summary")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("core:order-summary")

        

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False,
        vender=item.employee_id
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("core:order-summary")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.item.name+"\" remove from your cart")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("core:product", pk=pk)
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("core:product", pk = pk)


@login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This Item is not in your cart")
            return redirect("core:order-summary")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("core:order-summary")

def weekly_menu(request,pk):
    product=Product.objects.get(id=pk)
    print(product)
    emp=Employee.objects.get(user_id=product.employee)
    print(emp)
    data=Product.objects.filter(employee=emp.user_id)
    print(data)
    breakfast=""
    lunch=""
    dinner=""
    data1=''
    data2=''
    data3=''
    for obj in data:
        print(obj)
        ref=Product.objects.get(id=obj.id)
        print(ref)
        print(ref.category_id)
        if ref.category_id==1:
            breakfast=ref.id
            data1=Weekly_menu.objects.get(category_id=breakfast)
        elif  ref.category_id==2:
            lunch=ref.id
            data2=Weekly_menu.objects.get(category_id=lunch)
        elif ref.category_id==3:
            dinner=ref.id
            data3=Weekly_menu.objects.get(category_id=dinner)
    print(data1)
    print(data2)
    print(data3)
    context={
        "breakfast":data1,
        "lunch":data2,
        "dinner":data3
    }
    return render(request,'weekly_menu.html',context)