# ruff: noqa: F401 F811 F403
import pytest
from api.tests.fixtures.client import API_URL, api_client
from model_bakery import baker
from quizzes.enums import UserQuizStatus
from quizzes.models import QuizResult
from quizzes.tests.fixtures.quizzes import test_answer_options, test_questions, test_quizzes
from users.tests.fixtures.users import test_users

from companies.tests.fixtures.companies import test_company, test_company_members, test_owner
from companies.tests.fixtures.companies_client import owner_api_client


@pytest.mark.django_db
def test_get_last_completion_quiz_time_of_company_members(owner_api_client, 
                                                          test_company_members,
                                                          test_quizzes,
                                                          test_company):
    test_company_member_1 = test_company_members[0]
    test_company_member_2 = test_company_members[1]
    test_quiz = test_quizzes[0]

    test_company_member_1_quiz_result_1 : QuizResult = baker.make(
        QuizResult, quiz=test_quiz,
        status=UserQuizStatus.COMPLETED.value,
        user=test_company_member_1.user,
    )

    test_company_member_2_quiz_result_1 : QuizResult = baker.make(
        QuizResult, quiz=test_quiz,
        status=UserQuizStatus.COMPLETED.value,
        user=test_company_member_2.user,
    )

    test_request_1 = owner_api_client.get(
        f'{API_URL}/company_members/{test_company.id}/last_taken_quiz_times/'
    )
    assert test_request_1.status_code == 200
    assert test_request_1.data[0]['last_taken_quiz_time'] == test_company_member_1_quiz_result_1.updated_at
    assert test_request_1.data[1]['last_taken_quiz_time'] == test_company_member_2_quiz_result_1.updated_at

    # Make another request
    test_company_member_1_quiz_result_2 : QuizResult = baker.make(
        QuizResult, quiz=test_quiz,
        status=UserQuizStatus.COMPLETED.value,
        user=test_company_member_1.user,
    )

    test_company_member_2_quiz_result_2 : QuizResult = baker.make(
        QuizResult, quiz=test_quiz,
        status=UserQuizStatus.COMPLETED.value,
        user=test_company_member_2.user,
    )

    test_request_2 = owner_api_client.get(
        f'{API_URL}/company_members/{test_company.id}/last_taken_quiz_times/'
    )
    assert test_request_2.status_code == 200
    assert test_request_2.data[0]['last_taken_quiz_time'] == test_company_member_1_quiz_result_2.updated_at
    assert test_request_2.data[1]['last_taken_quiz_time'] == test_company_member_2_quiz_result_2.updated_at
