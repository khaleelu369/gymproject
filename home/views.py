from collections import UserDict
from django.shortcuts import render,redirect
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from product.models import UserProfile
from home.forms import SignupForm,UserProfileForm
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
#verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.
def index(request):
    return render(request,'user/index.html')

def about(request):
    return render(request,'user/about.html')

def blog_details(request):
    return render(request,'user/blog_details.html')

def blog(request):
    return render(request,'user/blog.html')

def contact(request):
    return render(request,'user/contact.html')

def courses(request):
    return render(request,'user/courses.html')

def elements(request):
    return render(request,'user/elements.html')

def gallery(request):
    return render(request,'user/gallery.html')

def main(request):
    return render(request,'user/main.html')

def pricing(request):
    return render(request,'user/pricing.html')

def verifi(request):
    return render(request,'user/verificationsuccess.html')


# def Signup(request):
#           if request.method=='POST':
#             print("aaaaa")
#             form=SignupForm(request.POST)
#             print('kskdkjdjfj')
#             if form.is_valid():
#                 email=form.cleaned_data.get('email')
#                 user=form.save()
#                 print("llllllllll")
#                 #useractivation
#                 current_site = get_current_site(request)
#                 mail_subject = "plese activate your account"
#                 message = render_to_string('user/verificationemail.html',{
#                     'user':user,
#                     'domain':current_site,
#                     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token':default_token_generator.make_token(user),
#                 })
#                 to_email=email
#                 send_email=EmailMessage(mail_subject,message,to=[to_email])
#                 send_email.send()
#                 messages.success(request,'Registration successful')

#                 return redirect('verifi')
#             else:
#                 print(form.errors)

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.save()
            
            # User activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('user/verificationemail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email], from_email=settings.EMAIL_HOST_USER)
            send_email.send()
            
            messages.success(request, 'Registration successful')
            return redirect('verifi')
        else:
            print(form.errors)
                    
               
    else:
        form=SignupForm()
    return render(request, 'user/signup.html',{'form':form})

def Login(request):
      if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully.')
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password.')
      else:
        form = AuthenticationForm()
      return render(request, 'user/login.html', {'form': form})
   
         
def activation(request,uidb64,token):
   try:
       uid = urlsafe_base64_decode(uidb64).decode()
       user = User._default_manager.get(pk=uid)
   except(TypeError,ValueError,OverflowError,User.DoesNotExist):
       user = None

   if user is not None and default_token_generator.check_token(user,token):
       user.is_active=True
       user.save()
       messages.success(request,'Congratulation Your account is activated.')
       return redirect('login')
   else:
       messages.error(request,'Invalid activation link')
       return redirect('signup')          

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password
            current_site = get_current_site(request)
            mail_subject = "Please reset password"
            message = render_to_string('user/resetpassword.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email], from_email=settings.EMAIL_HOST_USER)
            send_email.send()

            messages.success(request, 'Reset password link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotpassword')

    return render(request, 'user/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
       user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'please reset your password')
        return redirect('reset_password_email')
    else:
        messages.error(request,'This link has expired!')
        return redirect('login')
    
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password_email')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')

def reset_password_email(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_password_email')
    else:
        return render(request, 'user/reset_password_email.html')    
    


