from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import User


# To edit Django admin displaying user info and creating a user
class CustomUserAdmin(UserAdmin):
    model = User
    # Which fields will be displayed in Django admin when add user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 
                       'password1', 'password2', 'is_staff', 'image_path')
        }),
    )

# Register your models here.
admin.site.register(User, CustomUserAdmin)
