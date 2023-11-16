from companies.models import CompanyMembers
from django.utils import timezone

from meduzzen_backend.celery import app
from quizzes.models import Quiz


@app.task
def send_beat_reminder_quiz_notification():
    current_company_company_members = CompanyMembers.objects.all()

    for company_member in current_company_company_members:
        company_member_last_taken_quiz_times = Quiz.get_last_completions_time_of_quizzes(
            company_id=company_member.company.id,
            user_id=company_member.user.id
        )

        for quiz in company_member_last_taken_quiz_times:
            if quiz.last_taken_quiz_time:
                frequency_in_days = timezone.timedelta(days=quiz.frequency)

                if quiz.last_taken_quiz_time + frequency_in_days < timezone.now():
                    CompanyMembers.send_reminder_quiz_notification(
                        company_id=company_member.company.id,
                        quiz_name=quiz.title
                    )

            else:
                CompanyMembers.send_reminder_quiz_notification(
                        company_id=company_member.company.id,
                        quiz_name=quiz.title,
                        is_quiz_completed=False
                    )
