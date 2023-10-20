from api.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models

from .enums import CompanyInvitationStatus, CompanyMemberRole, Visibility

# User model
User = get_user_model()

# Create your models here.
class Company(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField(blank=False, null=False)
    visibility = models.CharField(max_length=15, 
                                  choices=Visibility.choices(), 
                                  default=Visibility.VISIBLE.value)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = 'Companies' # Plural naming

    def __str__(self):
        return self.name    


# All company requests to the users
class CompanyInvitations(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Company can't invite one user several times
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(default=CompanyInvitationStatus.PENDING.value, 
                              choices=CompanyInvitationStatus.choices())

    class Meta:
        verbose_name = "Company Invitation"
        verbose_name_plural = 'Company Invitations' # Plural naming

    def __str__(self):
        return f"{self.company} -> {self.user} - {self.status}"


# Company members
class CompanyMembers(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # User can't be in multiple companies
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(default=CompanyMemberRole.COMMON.value,
                            choices=CompanyMemberRole.choices())

    class Meta:
        verbose_name = "Company Member"
        verbose_name_plural = 'Company Members' # Plural naming

    def __str__(self):
        return f"{self.company} - {self.user}"
