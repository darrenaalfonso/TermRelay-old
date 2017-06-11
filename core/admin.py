from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'row_stamp']

admin.site.register(Company, CompanyAdmin)

