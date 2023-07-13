from django.urls import path
from . import views


urlpatterns = [
    path('products/',views.products,name='products'), 
    path('product1/',views.product1,name='product1'), 
    path('',views.base,name='base'),
    path('store/',views.store,name='store'), 
    path('protein/', views.protein, name='protein'), 
    path('leg/', views.leg, name='leg'), 
    path('fitnes/', views.fitnes, name='fitnes'), 
    path('weight/', views.weight, name='weight'), 
    path('running/', views.running, name='running'),
    path('cart/', views.cart, name='cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'), 
    path('product/<slug:category_slug>/', views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('place_order/',views.place_order,name='place_order'),
    path('myaccount/',views.myaccount,name='myaccount'),
    path('edit/',views.edit,name='edit'),
    path('ordersuccess/',views.ordersuccess,name='ordersuccess'),
    path('orders/',views.orders,name='orders'),
    path('search/',views.search,name='search'),
    path('bmi/',views.bmi,name='bmi'),
    path('bmi_result/',views.bmi_result,name='bmi_result'),
    
    
    
    
          

]