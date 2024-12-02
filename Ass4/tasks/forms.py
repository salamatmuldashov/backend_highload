from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Website

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'age', 'url']

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.strip() 

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0:
            raise forms.ValidationError("Age must be a positive integer")
        return age

    def clean_url(self):
        url = self.cleaned_data['url']
        return url.strip() 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
