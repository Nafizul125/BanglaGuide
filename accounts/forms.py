from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'age', 'gender', 'city', 'email', 'password1', 'password2')

class ProviderRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'age', 'gender', 'city', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')  # Use email for login