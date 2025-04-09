from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form."""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'Password'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'Email'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'Last Name'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')