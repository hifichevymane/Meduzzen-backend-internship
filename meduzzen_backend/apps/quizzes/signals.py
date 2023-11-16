from companies.models import CompanyMembers
from django.db.models.signals import post_save
from django.dispatch import receiver

from quizzes.models import Quiz


@receiver(signal=post_save, sender=Quiz)
def send_notifications_to_company_members(sender, instance: Quiz, created, **kwargs):
    if created:
        CompanyMembers.send_notifications_to_company_members(company_id=instance.company.id)
