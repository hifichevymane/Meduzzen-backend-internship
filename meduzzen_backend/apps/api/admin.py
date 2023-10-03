from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import User

# To edit Django admin displaying user info and creating a user
class CustomUserAdmin(UserAdmin):
    model = User

# Register your models here.
admin.site.register(User, CustomUserAdmin)
