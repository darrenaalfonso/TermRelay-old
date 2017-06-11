from django.contrib import admin
from .models import Company,Product


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'row_stamp']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'image', 'description', 'product_type', 'unit_description', 'price_per_unit']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
