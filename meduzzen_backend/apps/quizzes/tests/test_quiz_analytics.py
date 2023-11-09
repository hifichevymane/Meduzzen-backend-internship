# ruff: noqa: F401 F811 F403
import time

import pytest
from api.tests.fixtures.client import API_URL, api_client
from api.tests.pydantic.analytics import AnalyticsBody
from companies.tests.fixtures.companies import test_company
from companies.tests.fixtures.companies_client import owner_api_client, test_owner
from model_bakery import baker

from quizzes.enums import UserQuizStatus
from quizzes.models import QuizResult
from quizzes.tests.fixtures.quizzes import test_answer_options, test_owner, test_questions, test_quizzes


@pytest.mark.django_db
def test_get_quiz_rating(test_quizzes):
    test_quiz = test_quizzes[0]

    test_quiz_result_1 = baker.make(
        QuizResult, score=3, quiz=test_quiz, status=UserQuizStatus.COMPLETED.value
    )
    test_quiz_result_2 = baker.make(
        QuizResult, score=4, quiz=test_quiz, status=UserQuizStatus.COMPLETED.value
    )
    test_quiz_result_3 = baker.make(
        QuizResult, score=5, quiz=test_quiz, status=UserQuizStatus.COMPLETED.value
    )

    calculated_average = (test_quiz_result_1.score + test_quiz_result_2.score + test_quiz_result_3.score) / 3

    assert test_quiz.rating == calculated_average


@pytest.mark.django_db
def test_get_list_last_completions_time_of_quizzes(test_quizzes, owner_api_client, test_company):
    test_quiz_1, test_quiz_2 = test_quizzes

    test_quiz_1_result_1 = baker.make(
        QuizResult, quiz=test_quiz_1, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_quiz_2_result_1 = baker.make(
        QuizResult, quiz=test_quiz_2, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_request_1 = owner_api_client.get(f'{API_URL}/quizzes/{test_company.id}/last_completions_time/')
    assert test_request_1.status_code == 200
    request_data = test_request_1.data
    assert request_data[0]['last_taken_quiz_time'] == test_quiz_1_result_1.updated_at
    assert request_data[1]['last_taken_quiz_time'] == test_quiz_2_result_1.updated_at

    # Wait to make another request
    time.sleep(3)

    test_quiz_1_result_2 = baker.make(
        QuizResult, quiz=test_quiz_1, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_quiz_2_result_2 = baker.make(
        QuizResult, quiz=test_quiz_2, 
        status=UserQuizStatus.COMPLETED.value
    )

    test_request_2 = owner_api_client.get(f'{API_URL}/quizzes/{test_company.id}/last_completions_time/')
    assert test_request_2.status_code == 200
    request_data = test_request_2.data
    assert request_data[0]['last_taken_quiz_time'] == test_quiz_1_result_2.updated_at
    assert request_data[1]['last_taken_quiz_time'] == test_quiz_2_result_2.updated_at


@pytest.mark.django_db
def test_get_quizzes_average_scores(test_quizzes, owner_api_client):
    test_quiz_1, test_quiz_2 = test_quizzes

    test_quiz_1_result_1 = baker.make(
        QuizResult, quiz=test_quiz_1,
        score=10,
        status=UserQuizStatus.COMPLETED.value 
    )
    test_quiz_1_result_2 = baker.make(
        QuizResult, quiz=test_quiz_1,
        score=20,
        status=UserQuizStatus.COMPLETED.value 
    )

    test_quiz_2_result_1 = baker.make(
        QuizResult, quiz=test_quiz_2,
        score=10,
        status=UserQuizStatus.COMPLETED.value 
    )

    test_quiz_2_result_2 = baker.make(
        QuizResult, quiz=test_quiz_2,
        score=15,
        status=UserQuizStatus.COMPLETED.value 
    )

    test_quiz_1_average_score = (test_quiz_1_result_1.score + test_quiz_1_result_2.score) / 2
    test_quiz_2_average_score = (test_quiz_2_result_1.score + test_quiz_2_result_2.score) / 2

    # Make a request
    test_request_1_body = AnalyticsBody(
        start_date=test_quiz_1_result_1.updated_at,
        end_date=test_quiz_2_result_2.updated_at
    )

    test_request_1 = owner_api_client.post(
        f'{API_URL}/quizzes/analytics/', test_request_1_body.model_dump()
    )
    assert test_request_1.status_code == 200
    assert len(test_request_1.data) == 2
    assert test_request_1.data[0]['average_score'] == test_quiz_1_average_score
    assert test_request_1.data[1]['average_score'] == test_quiz_2_average_score

    test_quiz_1_result_3 = baker.make(
        QuizResult, quiz=test_quiz_1,
        score=50,
        status=UserQuizStatus.COMPLETED.value 
    )
    test_quiz_1_result_4 = baker.make(
        QuizResult, quiz=test_quiz_1,
        score=12,
        status=UserQuizStatus.COMPLETED.value 
    )

    test_quiz_2_result_3 = baker.make(
        QuizResult, quiz=test_quiz_2,
        score=14,
        status=UserQuizStatus.COMPLETED.value 
    )

    test_quiz_2_result_4 = baker.make(
        QuizResult, quiz=test_quiz_2,
        score=27,
        status=UserQuizStatus.COMPLETED.value 
    )

    test_request_2_body = AnalyticsBody(
        start_date=test_quiz_1_result_3.updated_at,
        end_date=test_quiz_2_result_4.updated_at
    )

    test_quiz_1_average_score = (test_quiz_1_result_3.score + test_quiz_1_result_4.score) / 2
    test_quiz_2_average_score = (test_quiz_2_result_3.score + test_quiz_2_result_4.score) / 2

    test_request_2 = owner_api_client.post(
        f'{API_URL}/quizzes/analytics/', test_request_2_body.model_dump()
    )
    assert test_request_2.status_code == 200
    assert len(test_request_2.data) == 2
    assert test_request_2.data[0]['average_score'] == test_quiz_1_average_score
    assert test_request_2.data[1]['average_score'] == test_quiz_2_average_score
