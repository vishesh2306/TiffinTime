
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import Feedback

class ContactForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    messege=forms.TimeField(required=True)
    

    class Meta(UserCreationForm.Meta):
         model = Feedback

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.phone=self.cleaned_data.get('phone')
        user.messege=self.cleaned_data.get('messege')
        user.save()
        return user
