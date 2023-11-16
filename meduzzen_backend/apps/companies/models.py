from api.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from notifications.models import Notifications
from quizzes.models import QuizResult

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
    role = models.CharField(default=CompanyMemberRole.MEMBER.value,
                            choices=CompanyMemberRole.choices())
    
    @staticmethod
    def get_last_taken_quiz_times(company_id: int):
        last_quiz_time_subquery = QuizResult.filter_last_quiz_results(
            is_company_members_model_subquery=True
        )

        queryset = CompanyMembers.objects.filter(company_id=company_id).annotate(
            last_taken_quiz_time=models.Subquery(last_quiz_time_subquery)
        ).values('user', 'last_taken_quiz_time')

        return queryset
    
    @staticmethod
    def get_company_user_works_in(user_id: int) -> QuerySet:
        return CompanyMembers.objects.filter(user_id=user_id)
    
    @staticmethod
    def create_notifications_to_company_members(company_id: int) -> None:
        company_members = CompanyMembers.objects.filter(company_id=company_id)
        company_members_notifications_list: list[Notifications] = []

        for company_member in company_members:
            company_member_notification = Notifications(
                user=company_member.user,
                text='New quiz was created. Check it out'
            )
            company_members_notifications_list.append(company_member_notification)
        
        Notifications.objects.bulk_create(company_members_notifications_list)
    
    @staticmethod
    def create_reminder_quiz_notification(
        company_id: int,
        quiz_name: str,
        is_quiz_completed: bool = True
    ) -> None:
        company_members = CompanyMembers.objects.filter(company_id=company_id)

        reminder_quiz_notifications_list: list[Notifications] = []
        
        for company_member in company_members:
            if is_quiz_completed:
                notification_text = f'Do you want to undergo {quiz_name} quiz?'
            else:
                notification_text = f'You have not completed {quiz_name} quiz yet. Wanna undergo?'

            reminder_quiz_notification = Notifications(
                user=company_member.user,
                text=notification_text
            )

            reminder_quiz_notifications_list.append(reminder_quiz_notification)
        
        Notifications.objects.bulk_create(reminder_quiz_notifications_list)

    class Meta:
        verbose_name = "Company Member"
        verbose_name_plural = 'Company Members' # Plural naming

    def __str__(self):
        return f"{self.company} - {self.user}"


class CompanyUserRating(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avarage_score = models.FloatField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = "Company User Rating"
        verbose_name_plural = 'Company User Ratings'

    def __str__(self):
        return f"{self.company} - {self.user} - {self.avarage_score}"
