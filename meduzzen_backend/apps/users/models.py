from enum import Enum

from api.models import TimeStampedModel
from companies.models import Company
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Status choices for UsersRequests models
class UsersRequestStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    REVOKED = 'revoked'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


# Create your models here.

class UsersRequests(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Company can't invite one user several times
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(default=UsersRequestStatus.PENDING.value, 
                              choices=UsersRequestStatus.choices())

    class Meta:
        verbose_name = "Users Request"
        verbose_name_plural = 'Users Requests' # Plural naming

    def __str__(self):
        return f"{self.user} -> {self.company} - {self.status}"
