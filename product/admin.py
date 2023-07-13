from django.contrib import admin
from .models import category
from .models import product
from .models import Cart,CartItem
from .models import Order,OrderProduct,Payment
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.utils.html import format_html




class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','slug')
# Register your models here.
admin.site.register(category,categoryAdmin)


class productAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}


class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','first_name','phone','email','city','order_total','tax','status','is_ordered','created_at']
    list_filter=['status','is_ordered']
    search_fields=['order_number','first_name','last_name','phone','email']
    list_per_page=20


admin.site.register(product,productAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)


User = get_user_model()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(UserProfile, UserProfileAdmin)
