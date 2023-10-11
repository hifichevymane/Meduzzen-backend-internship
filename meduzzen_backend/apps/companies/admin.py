from django.contrib import admin

from .models import Company


# CompanyAdmin class for Django Admin
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description') # searching
    list_filter = ('owner', 'name') # filtering

# Register your models here.
admin.site.register(Company, CompanyAdmin)
