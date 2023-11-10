# ruff: noqa: F401 F811 F403
import pytest
from api.tests.fixtures.client import API_URL, api_client
from companies.tests.fixtures.companies import test_company
from companies.tests.fixtures.companies_client import owner_api_client, test_owner

from quizzes.models import AnswerOption, Question, Quiz, QuizResult, UserQuizStatus, UsersAnswer
from quizzes.tests.fixtures.quizzes import test_answer_options, test_questions, test_quizzes
from quizzes.tests.schemas.quizzes import (
    AnswerOptionRequestBodySchema,
    QuestionRequestBodySchema,
    QuizRequestBodySchema,
    QuizResultRequestBodySchema,
    UserAnswerRequestBodySchema,
)


@pytest.mark.parametrize('option_text', ['Yes', 'No'])
@pytest.mark.django_db
def test_create_answer_options(option_text, owner_api_client):
    test_option = AnswerOptionRequestBodySchema(text=option_text)

    request = owner_api_client.post(f"{API_URL}/answer_options/", test_option.model_dump())
    assert request.status_code == 201
    assert AnswerOption.objects.get(pk=request.data['id'])


@pytest.mark.django_db
def test_create_question(owner_api_client, test_answer_options):
    test_option_1, test_option_2 = test_answer_options

    test_question = QuestionRequestBodySchema(
        text="Are you gay?",
        options=[test_option_1.id, test_option_2.id],
        answer=[test_option_1.id,]
    )

    request = owner_api_client.post(f'{API_URL}/questions/', test_question.model_dump())
    assert request.status_code == 201
    assert Question.objects.get(pk=request.data['id'])


@pytest.mark.django_db
def test_create_quiz(owner_api_client, test_questions, test_company):
    test_question_1, test_question_2 = test_questions
    test_quiz_payload = QuizRequestBodySchema(
        company=test_company.id,
        title="Gay test",
        description="Gay test",
        questions= [test_question_1.id, test_question_2.id]
    )

    request = owner_api_client.post(f'{API_URL}/quizzes/', test_quiz_payload.model_dump())
    assert request.status_code == 201
    assert Quiz.objects.get(pk=request.data['id'])


@pytest.mark.django_db
def test_undergo_quiz(owner_api_client, test_quizzes, test_questions, test_answer_options):
    test_quiz = test_quizzes[0]

    start_test_request_payload = QuizResultRequestBodySchema(quiz=test_quiz.id)

    # Send POST request to start the quiz
    start_quiz_request = owner_api_client.post(
        f'{API_URL}/quiz_results/',
        start_test_request_payload.model_dump()
    )
    assert start_quiz_request.status_code == 201

    test_quiz_result = QuizResult.objects.get(pk=start_quiz_request.data['id'])
    assert test_quiz_result
    assert test_quiz_result.status == UserQuizStatus.PENDING.value


    test_question_1, test_question_2 = test_questions
    test_answer_option_1 = test_answer_options[0]

    test_user_answer_payload_1 = UserAnswerRequestBodySchema(
        quiz=test_quiz.id,
        question=test_question_1.id,
        answer=[test_answer_option_1.id],
        quiz_result=test_quiz_result.id
    )

    # Create a user answer to a question
    test_user_answer_request_1 = owner_api_client.post(
        f'{API_URL}/users_answers/', 
        test_user_answer_payload_1.model_dump()
    )
    assert test_user_answer_request_1.status_code == 201

    user_answer_1 = UsersAnswer.objects.get(pk=test_user_answer_request_1.data['id'])
    assert user_answer_1
    assert user_answer_1.is_correct

    test_user_answer_payload_2 = UserAnswerRequestBodySchema(
        quiz=test_quiz.id,
        question=test_question_2.id,
        answer=[test_answer_option_1.id],
        quiz_result=test_quiz_result.id
    )

    test_user_answer_request_2 = owner_api_client.post(
        f'{API_URL}/users_answers/', 
        test_user_answer_payload_2.model_dump()
    )
    assert test_user_answer_request_2.status_code == 201
    user_answer_2 = UsersAnswer.objects.get(pk=test_user_answer_request_2.data['id'])
    assert user_answer_2
    assert user_answer_2.is_correct

    # PATCH request to set status to completed
    test_complete_test_request = owner_api_client.patch(f'{API_URL}/quiz_results/{test_quiz_result.id}/')
    assert test_complete_test_request.status_code == 200
    # Check if status of quiz_result is completed
    assert test_complete_test_request.data['status'] == UserQuizStatus.COMPLETED.value
    assert test_complete_test_request.data['score'] == 2 # Check if answers were right
