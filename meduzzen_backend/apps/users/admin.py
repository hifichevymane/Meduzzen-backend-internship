from django.contrib import admin

from .models import UsersRequests


class UsersRequestsAdmin(admin.ModelAdmin):
    search_fields = ('company', 'user')
    list_filter = ('company', 'user')

admin.site.register(UsersRequests, UsersRequestsAdmin)
