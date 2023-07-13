from django.shortcuts import render,redirect,get_object_or_404
from .models import product,category,Cart,CartItem,Order,UserProfile,Payment,OrderProduct
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseNotAllowed
from home.forms import SignupForm,UserProfileForm
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
# from .razorpay_integration import process_payment
# import razorpay
import json





def products(request):
     products = product.objects.all().filter(is_available=True)

     context ={
          'products':products,
     }
     return render(request,'product.html',context)

def protein(request):
     protein_category = category.objects.get(category_name='Protein Powder')
     protein_products = product.objects.filter(category=protein_category, is_available=True)
     return render(request, 'protein.html', {'prod': protein_products})

def leg(request):
     leg_category = category.objects.get(category_name='Leg')
     leg_products = product.objects.filter(category=leg_category, is_available=True)
     return render(request, 'legproduct.html', {'legprod': leg_products})

def fitnes(request):
     fitnes_category = category.objects.get(category_name='Fitnes')
     fitnes_products = product.objects.filter(category=fitnes_category, is_available=True)
     return render(request, 'fitnesproduct.html', {'fitnesprod': fitnes_products})

def weight(request):
     weight_category = category.objects.get(category_name='Weight')
     weight_products = product.objects.filter(category=weight_category, is_available=True)
     return render(request, 'weightproduct.html', {'weightprod': weight_products})

def running(request):
     running_category = category.objects.get(category_name='Running Mechine')
     running_products = product.objects.filter(category=running_category, is_available=True)
     return render(request, 'runningproduct.html', {'runningprod': running_products})

def base(request):
     return render(request,'base.html')


def product1(request):
     return render(request,'products1.html')

def store(request, category_slug):
    cat = get_object_or_404(category, slug=category_slug)
    products = cat.product_set.all() 
    
    context = {
        'productstore': products,
    }
    
    return render(request, 'store.html', context)


# def product_detail(request,category_slug,product_slug):
#      try:
#           single_product=product.objects.get(category__slug=category_slug,slug=product_slug)
#      except Exception as e:
#           raise e
     
#      context ={
#           'single_product':single_product,
#      }     
#      return render(request,'product-detail.html',context)      

def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(product, category__slug=category_slug, slug=product_slug)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    context = {
        'single_product': single_product,
        'in_cart' : in_cart,
    }
    return render(request, 'product-detail.html', context)



def _cart_id(request):
     cart = request.session.session_key
     if not cart:
          cart=request.session.create()
     return cart

def add_cart(request,product_id):
     selected_product = product.objects.get(id=product_id)#get the product
     print(product_id)
     try:    
          cartt=Cart.objects.get(cart_id=_cart_id(request)) #get the cart using cart_id
     except Cart.DoesNotExist:
          cartt=Cart.objects.create(cart_id=_cart_id(request))
     cartt.save()
     cart_item=None
     try:
          cart_item=CartItem.objects.get(product=selected_product,cart=cartt)
          cart_item.quantity += 1
          cart_item.save()
     except CartItem.DoesNotExist:
          cart_item = CartItem.objects.create(
               product=selected_product,
               quantity=1,
               cart=cartt,
          )
          cart_item.save()
     return redirect('cart')

def remove_cart(request,product_id):
     cart = Cart.objects.get(cart_id=_cart_id(request))
     Product=get_object_or_404(product,id=product_id)
     cart_item=CartItem.objects.get(product=Product,cart=cart) 
     if cart_item.quantity>1:
          cart_item.quantity -=1
          cart_item.save()
     else:
          cart_item.delete()
     return redirect('cart') 

def remove_cart_item(request,product_id):
     cart = Cart.objects.get(cart_id=_cart_id(request))
     Product=get_object_or_404(product,id=product_id)
     cart_item=CartItem.objects.get(product=Product,cart=cart) 
     cart_item.delete()
     return redirect('cart')
        


def cart(request,total=0,quantity=0,cart_items=None):
     tax = 0  
     grand_total = 0
     try:
          car=Cart.objects.get(cart_id=_cart_id(request))
          cart_items=CartItem.objects.filter(cart=car,is_active=True)
          for car_t in cart_items:
               total += (car_t.product.price * car_t.quantity)
               quantity += car_t.quantity
          tax=(2*total)/100
          grand_total=total+tax
     except ObjectDoesNotExist:
          pass          
    
     context ={
          'total':total,
          'quantity':quantity,
          'cart_items':cart_items,
          'tax':tax,
          'grand_total':grand_total,
     }
     return render(request,'cart.html', context)





def checkout(request,total=0,quantity=0,cart_items=None):
     tax = 0  
     grand_total = 0 
     try:
          car=Cart.objects.get(cart_id=_cart_id(request))
          cart_items=CartItem.objects.filter(cart=car,is_active=True)
          for car_t in cart_items:
               total += (car_t.product.price * car_t.quantity)
               quantity += car_t.quantity
          tax=(2*total)/100
          grand_total=total+tax
     except ObjectDoesNotExist:
          pass          
    
     context ={
          'total':total,
          'quantity':quantity,
          'cart_items':cart_items,
          'tax':tax,
          'grand_total':grand_total,
         }
     return render(request,'checkout.html', context)


def payment(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
        payment_obj = Payment(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=order.order_total,
            status=body['status'],
        )
        payment_obj.save()

        order.payment = payment_obj
        order.is_ordered = True
        order.save()

        # Move the cart items to order product table
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.Payment = payment_obj  
            orderproduct.user_id = request.user.id  
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # Reduce the quantity of the sold products
            products = product.objects.get(id=item.product_id)
            products.stock -= item.quantity
            products.save()

        # Clear cart
        CartItem.objects.filter(cart=cart).delete()

        #email
        mail_subject = "thank you for your purchase"
        message = render_to_string('order_recieve_email.html',{
               'user':request.user,
               'order':order,
                })
        to_email=request.user.email
        send_email=EmailMessage(mail_subject,message,to=[to_email])
        send_email.send()

        # redirect to success page
        data={
             'order_number':order.order_number,
             'transID': payment_obj.payment_id,
        } 
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(['POST'])


    

           

# @login_required 
# def place_order(request, total=0, quantity=0):
#     current_user = request.user
#     cart = Cart.objects.get(cart_id=_cart_id(request))
#     cart_items = CartItem.objects.filter(cart=cart)
#     cart_count = cart_items.count()
    
#     if cart_count <= 0:
#         return redirect('store')
    
#     grand_total = 0
#     tax = 0
    
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
    
#     tax = (2 * total) / 100
#     grand_total = total + tax
    
#     if request.method == 'POST':
#         print('=============')
#         print(request.POST)
#         form = OrderForm(request.POST)
        
#         if form.is_valid():
#             data = form.cleaned_data
            
#             order = Order()
#             order.user = current_user.username
#             order.first_name = data['first_name']
#             order.last_name = data['last_name']
#             order.phone = data['phone']
#             order.email = data['email']
#             order.address_line_1 = data['address_line_1']
#             order.address_line_2 = data['address_line_2']
#             order.country = data['country']
#             order.state = data['state']
#             order.city = data['city']
#             order.order_note = data['order_note']
#             order.order_total = grand_total
#             order.tax = tax
#             order.ip = request.META.get('REMOTE_ADDR')
#             order.save()
            
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr, mt, dt)
#             current_date = d.strftime("%Y%m%d")
#             order_number = current_date + str(order.id)
#             order.order_number = order_number
#             order.save()
            
#             try:
#                 order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
#                 context = {
#                     'order': order,
#                     'cart_items': cart_items,
#                     'total': total,
#                     'tax': tax,
#                     'grand_total': grand_total,
#                 }

#                 return render(request, 'payment.html', context)
#             except Order.DoesNotExist:
#                 return HttpResponse('Order does not exist.')
#     else:
#         return redirect('checkout')
#     return HttpResponseNotAllowed(['POST'])



@login_required
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = cart_items.count()
    
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            order = Order()
            order.user = current_user.username
            order.first_name = data['first_name']
            order.last_name = data['last_name']
            order.phone = data['phone']
            order.address_line_1 = data['address_line_1']
            order.address_line_2 = data['address_line_2']
            order.country = data['country']
            order.state = data['state']
            order.city = data['city']
            order.order_note = data['order_note']
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            
            try:
                validate_email(data['email'])  # Validate email format
                order.email = data['email']
                order.save()
            except ValidationError:
                return HttpResponse('Invalid email address')
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()
            
            try:
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total,
                }

                return render(request, 'payment.html', context)
            except Order.DoesNotExist:
                return HttpResponse('Order does not exist.')
        else:
            print(form.errors)  # Print form errors to console for debugging
            return HttpResponse('Invalid form data')  # Return a response for invalid form data
    else:
        return redirect('checkout')


def myaccount(request):
     # userprofile=UserProfile.objects.get(user_id=request.user.id)
     # context={
     #      'userprofile':userprofile,
     # }     
     return render(request,'myaccount.html')

def edit(request):
     userprofile=get_object_or_404(UserProfile,user=request.user)
     if request.method=='POST':
          user_form=SignupForm(request.POST,instance=request.user)
          profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
          if user_form.is_valid() and profile_form.is_valid():
               user_form.save()
               profile_form.save()
               messages.success(request,'Your profile has been updated')
               return redirect('edit')
     else:
          user_form=SignupForm(instance=request.user)
          profile_form=UserProfileForm(instance=userprofile)
     context={
          'user_form':user_form,
          'profile_form':profile_form,
          'userprofile':userprofile,
     }     
     return render(request,'editprofile.html',context)
  
def ordersuccess(request):
     return render(request,'ordersuccess.html')  

def orders(request):
     orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
     context={
          'orders':orders,
     }
     return render(request,'orders.html',context)



def search(request):
    keyword = request.GET.get('keyword')
    category_slug = request.GET.get('category_slug')

    products = product.objects.order_by('-created_date')

    if keyword:
        products = products.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

    if category_slug:
        products = products.filter(category__slug=category_slug)

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'search_results.html', context)

# def search(request):
#      if 'keyword' in request.GET:
#           keyword=request.GET['keyword']
#           if keyword:
#                products=product.objects.order_by('-created_date').filter(Q(description=keyword) | Q(product_name=keyword))
#                product_count=products.count()
#      context={
#           'products':products,
#           'product_count':product_count,
#      }          
#      return HttpResponse('search page',context)

def bmi(request):
     
    if request.method == 'POST':
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        age = int(request.POST['age'])
        sex = request.POST['sex']

        # BMI calculation
        height_in_meters = height / 100  # Convert height from cm to meters
        bmi = weight / (height_in_meters ** 2)

        # Determine weight status
        if bmi < 18.5:
            weight_status = 'Underweight'
        elif 18.5 <= bmi <= 24.9:
            weight_status = 'Healthy'
        elif 25.0 <= bmi <= 29.9:
            weight_status = 'Overweight'
        else:
            weight_status = 'Obese'

        context = {
            'bmi': bmi,
            'weight_status': weight_status,
        }
        return render(request, 'bmi_result.html', context)

    return render(request,'bmi.html')

def bmi_result(request):
     return render(request,'bmi_result')