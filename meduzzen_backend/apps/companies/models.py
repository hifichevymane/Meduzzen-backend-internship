from api.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models

# User model
User = get_user_model()

# Status choices for CompanyRequests and UsersRequests models
class Status(models.TextChoices):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


# Visibility choices 
class Visibility(models.TextChoices):
    VISIBLE = 'visible'
    HIDDEN = 'hidden'


# Request type choices
class RequestType(models.TextChoices):
    COMPANY_TO_USER = 'company to user'
    USER_TO_COMPANY = 'user to company'


# Create your models here.
class Company(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField(blank=False, null=False)
    visibility = models.CharField(max_length=15, 
                                  choices=Visibility.choices, 
                                  default=Visibility.VISIBLE)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = 'Companies' # Plural naming

    def __str__(self):
        return self.name    


# All company requests to the users
class CompanyRequests(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Company can't invite one user several times
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(default=Status.PENDING, choices=Status.choices)
    # Determine if it's user's request to the company or company's request
    request_type = models.CharField(blank=False, null=False, choices=RequestType.choices)

    class Meta:
        verbose_name = "Company Request"
        verbose_name_plural = 'Company Requests' # Plural naming

    def __str__(self):
        if self.request_type == RequestType.COMPANY_TO_USER:
            return f"{self.company} -> {self.user} - {self.status}"
        else:
            return f"{self.user} -> {self.company} - {self.status}"


# Company members
class CompanyMembers(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # User can't be in multiple companies
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Company Member"
        verbose_name_plural = 'Company Members' # Plural naming

    def __str__(self):
        return f"{self.company} - {self.user}"
