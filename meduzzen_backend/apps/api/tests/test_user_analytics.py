# ruff: noqa: F401 F811 F403
import pytest
from companies.tests.fixtures.companies import test_company, test_owner
from model_bakery import baker
from quizzes.enums import UserQuizStatus
from quizzes.models import QuizResult
from quizzes.tests.fixtures.quizzes import test_answer_options, test_questions, test_quizzes
from users.tests.fixtures.user_client import user_api_client
from users.tests.fixtures.users import test_users

from api.tests.fixtures.client import API_URL, api_client
from api.tests.schemas.analytics import AnalyticsRequestBodySchema


@pytest.mark.django_db
def test_user_analytics(user_api_client, test_users, test_quizzes):
    test_user_1, test_user_2 = test_users[0], test_users[1]
    test_quiz = test_quizzes[0]

    test_user_1_result_1 = baker.make(
        QuizResult, score=20, quiz=test_quiz,
        user=test_user_1, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_1_result_2 = baker.make(
        QuizResult, score=20, quiz=test_quiz,
        user=test_user_1,
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_1_average_score = (test_user_1_result_1.score + test_user_1_result_2.score) / 2

    test_user_2_result_1 = baker.make(
        QuizResult, score=50, quiz=test_quiz,
        user=test_user_2, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_2_result_2 = baker.make(
        QuizResult, score=50, quiz=test_quiz,
        user=test_user_2,
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_2_average_score = (test_user_2_result_1.score + test_user_2_result_2.score) / 2

    test_request_1_body = AnalyticsRequestBodySchema(
        start_date=test_user_1_result_1.updated_at,
        end_date=test_user_2_result_2.updated_at
    )

    test_request_1 = user_api_client.post(
        f'{API_URL}/users/analytics/', test_request_1_body.model_dump()
    )
    assert test_request_1.status_code == 200
    assert test_request_1.data[0]['average_score'] == test_user_1_average_score
    assert test_request_1.data[1]['average_score'] == test_user_2_average_score

    # Make another request to check the difference
    test_user_1_result_3 = baker.make(
        QuizResult, score=30, quiz=test_quiz,
        user=test_user_1, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_1_result_4 = baker.make(
        QuizResult, score=30, quiz=test_quiz,
        user=test_user_1,
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_1_average_score = (test_user_1_result_3.score + test_user_1_result_4.score) / 2

    test_user_2_result_3 = baker.make(
        QuizResult, score=50, quiz=test_quiz,
        user=test_user_2, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_2_result_4 = baker.make(
        QuizResult, score=50, quiz=test_quiz,
        user=test_user_2,
        status=UserQuizStatus.COMPLETED.value
    )

    test_user_2_average_score = (test_user_2_result_3.score + test_user_2_result_4.score) / 2

    test_request_2_body = AnalyticsRequestBodySchema(
        start_date=test_user_1_result_3.updated_at,
        end_date=test_user_2_result_4.updated_at
    )

    test_request_2 = user_api_client.post(
        f'{API_URL}/users/analytics/', test_request_2_body.model_dump()
    )
    assert test_request_2.status_code == 200
    assert test_request_2.data[0]['average_score'] == test_user_1_average_score
    assert test_request_2.data[1]['average_score'] == test_user_2_average_score


@pytest.mark.django_db
def test_selected_user_analytics(user_api_client, test_users, test_quizzes):
    test_user = test_users[0]
    test_quiz_1, test_quiz_2 = test_quizzes

    test_quiz_1_result_1 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_1,
        status=UserQuizStatus.COMPLETED.value,
        score=50
    )

    test_quiz_1_result_2 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_1,
        status=UserQuizStatus.COMPLETED.value,
        score=50
    )

    test_quiz_1_avg_score = (test_quiz_1_result_1.score + test_quiz_1_result_2.score) / 2

    test_quiz_2_result_1 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_2,
        status=UserQuizStatus.COMPLETED.value,
        score=15
    )

    test_quiz_2_result_2 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_2,
        status=UserQuizStatus.COMPLETED.value,
        score=15
    )

    test_quiz_2_avg_score = (test_quiz_2_result_1.score + test_quiz_2_result_2.score) / 2

    test_request_1_body = AnalyticsRequestBodySchema(
        start_date=test_quiz_1_result_1.updated_at,
        end_date=test_quiz_2_result_2.updated_at
    )

    test_request_1 = user_api_client.post(
        f'{API_URL}/quizzes/{test_user.id}/selected_user_analytics/',
        test_request_1_body.model_dump()
    )
    assert test_request_1.status_code == 200
    assert test_request_1.data[0]['average_score'] == test_quiz_1_avg_score
    assert test_request_1.data[1]['average_score'] == test_quiz_2_avg_score

    # Create another quiz_results
    test_quiz_1_result_3 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_1,
        status=UserQuizStatus.COMPLETED.value,
        score=77
    )

    test_quiz_1_result_4 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_1,
        status=UserQuizStatus.COMPLETED.value,
        score=77
    )

    test_quiz_1_avg_score = (test_quiz_1_result_3.score + test_quiz_1_result_4.score) / 2

    test_quiz_2_result_3 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_2,
        status=UserQuizStatus.COMPLETED.value,
        score=45
    )

    test_quiz_2_result_4 = baker.make(
        QuizResult, user=test_user, quiz=test_quiz_2,
        status=UserQuizStatus.COMPLETED.value,
        score=45
    )

    test_quiz_2_avg_score = (test_quiz_2_result_3.score + test_quiz_2_result_4.score) / 2

    test_request_2_body = AnalyticsRequestBodySchema(
        start_date=test_quiz_1_result_3.updated_at,
        end_date=test_quiz_2_result_4.updated_at
    )

    test_request_2 = user_api_client.post(
        f'{API_URL}/quizzes/{test_user.id}/selected_user_analytics/',
        test_request_2_body.model_dump()
    )
    assert test_request_2.status_code == 200
    assert test_request_2.data[0]['average_score'] == test_quiz_1_avg_score
    assert test_request_2.data[1]['average_score'] == test_quiz_2_avg_score
