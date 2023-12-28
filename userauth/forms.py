from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username', 'email']
