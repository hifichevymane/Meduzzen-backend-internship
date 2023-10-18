from django.contrib import admin

from companies import models


# CompanyAdmin class for Django Admin
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description') # searching
    list_filter = ('owner', 'name') # filtering


class CompanyInvitationsAdmin(admin.ModelAdmin):
    search_fields = ('company', 'user')
    list_filter = ('company', 'user', 'status')


class CompanyMembersAdmin(admin.ModelAdmin):
    search_fields = ('company', 'user')
    list_filter = ('company', 'user')

# Register your models here.
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.CompanyInvitations, CompanyInvitationsAdmin)
admin.site.register(models.CompanyMembers, CompanyMembersAdmin)
