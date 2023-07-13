from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('blog_details/',views.blog_details,name='blogdet'),
    path('blog/',views.blog),
    path('contact/',views.contact,name='contact'),
    path('courses/',views.courses,name='courses'),
    path('elements/',views.elements),
    path('gallery/',views.gallery,name='gallery'),
    path('main/',views.main),
    path('pricing/',views.pricing,name='pricing'),
    path('signup/',views.Signup,name='signup'),
    path('login/',views.Login,name='login'),
    path('activation/<uidb64>/<token>/',views.activation,name='activation'),
    path('verifi/',views.verifi,name='verifi'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('reset_password_email/',views.reset_password_email,name='reset_password_email'),
    
]
