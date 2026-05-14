from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'customer_name',
            'email',
            'garment_type',
            'alteration_type',
            'notes',
            'image',
            'deadline',
            'image',
        ]

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        from django import forms
from .models import Order

class HomeImageUploadForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "email", "garment_type", "image"]
