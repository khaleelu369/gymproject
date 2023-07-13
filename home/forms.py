from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.contrib.auth.forms import UserCreationForm
from product.models import UserProfile





  
    
# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2') 

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         username = cleaned_data.get('username')
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')

#         if email and User.objects.filter(email=email).exists():
#             raise forms.ValidationError('This email address is already in use.')
#         if username and User.objects.filter(username=username).exists():
#             raise forms.ValidationError('This username is already taken.')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('The passwords do not match.')

#         return cleaned_data
    

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_number = forms.CharField(max_length=15, help_text='Required')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username[0].isalpha():
            raise forms.ValidationError('Username must start with a letter.')
        if not username.isalpha():
            raise forms.ValidationError('Username must only contain letters.')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords do not match.')
        
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('user','address_line1','address_line2','city','state','country','profile_picture')
