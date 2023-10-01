from django.urls import path
from . import views
from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    ProductView,
    #HomeView,
    OrderSummaryView,
    CheckoutView,
    PaymentView,
    menu,
    weekly_menu,
    update_duration,
    OrderSuccess
)

app_name = 'core'

urlpatterns = [
    #path('', HomeView.as_view(), name='home'),
    path('',views.menu),
    path('product/<pk>/', ProductView.as_view(), name='product'),
    path('weekly-menu/<pk>/', weekly_menu, name='weekly-menu'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order_success/', OrderSuccess.as_view(), name='order_success'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('update_duration/<pk>/', update_duration, name='update_duration'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', reduce_quantity_item, name='reduce-quantity-item')
]


