from django.contrib import admin

# Register your models here.

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'image']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product)
# admin.site.register(AdminProduct)
# admin.site.register(AdminCategory)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
