from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class category(models.Model):
    category_name=models.CharField(max_length=100, unique=True)
    slug=models.SlugField(max_length=100, unique=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)
    
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])


    def __str__(self):
        return self.category_name
    

class product(models.Model):
    product_name =models.CharField(max_length=200,unique=True)
    slug =models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField()
    images=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    modified_date=models.DateField(auto_now=True)  
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.product_name 
    
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    cart =models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity =models.IntegerField()
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def  __str__(self):
        return self.product
    
#payment    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method= models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order (models.Model):
    STATUS = (
            ('New', 'New'),
            ('Accepted', 'Accepted'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        )

    user=models.CharField(max_length=50)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models. EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50) 
    state = models.CharField(max_length=50)
    city= models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip= models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'

    # def __str__(self):
    #     return self.first_name 



    
class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_products')
    Payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True,related_name='order_products')
    # user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='order_products')
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    # variation=models.ForeignKey(Variation,on_delete=models.CASCADE)
    # flavour=models.CharField(max_length=50)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
class UserProfile(models.Model):
    user=models.OneToOneField(Order,on_delete=models.CASCADE)
    address_line1=models.CharField(blank=True,max_length=100)
    address_line2=models.CharField(blank=True,max_length=100)
    profile_picture=models.ImageField(blank=True,upload_to='userprofile')
    city=models.CharField(blank=True,max_length=20)
    state=models.CharField(blank=True,max_length=20) 
    country=models.CharField(blank=True,max_length=20)

    def __str__(self):
        return self.user.first_name
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'