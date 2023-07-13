from django.urls import path
from . import views

urlpatterns = [
    path('packages/',views.packages,name='packages'), 
    path('package/package_payment/<int:plan_id>/',views.package_payment,name='package_payment'),
    path('package/payment_success/', views.payment_success, name='payment_success'),
    path('package/payment_error/', views.payment_error, name='payment_error'),
    path('cancel_plan/<int:plan_id>/', views.cancel_plan, name='cancel_plan'),
    path('package/current_plan', views.current_plan, name='current_plan'),
]