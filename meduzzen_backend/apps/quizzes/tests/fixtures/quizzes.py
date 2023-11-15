# ruff: noqa: F401 F811 F403
import pytest
from companies.tests.fixtures.companies import test_owner
from model_bakery import baker
from users.tests.fixtures.users import test_users

from quizzes.enums import UserQuizStatus
from quizzes.models import AnswerOption, Question, Quiz, QuizResult


@pytest.fixture
def test_answer_options():
    test_option_1: AnswerOption = baker.make(AnswerOption, text='Yes')
    test_option_2: AnswerOption = baker.make(AnswerOption, text='No')

    return test_option_1, test_option_2


@pytest.fixture
def test_questions(test_answer_options, test_owner):
    test_question_1: Question = baker.make(
        Question, 
        text='Are you gay?', 
        options=test_answer_options, 
        answer=[test_answer_options[0]],
        creator=test_owner
    )
    
    test_question_2: Question = baker.make(
        Question,
        text='Do you love Death Grips?',
        options=test_answer_options, 
        answer=[test_answer_options[0]],
        creator=test_owner
    )
    
    return test_question_1, test_question_2


@pytest.fixture
def test_quizzes(test_questions, test_owner, test_company):
    test_quiz_1: Quiz = baker.make(
        Quiz, 
        creator=test_owner,
        company=test_company,
        questions=test_questions,
    )

    test_quiz_2: Quiz = baker.make(
        Quiz, 
        creator=test_owner,
        company=test_company,
        questions=test_questions,
    )

    return test_quiz_1, test_quiz_2


@pytest.fixture
def test_quiz_results(test_company, test_users, test_quizzes):
    test_user = test_users[0]
    test_quiz_1, test_quiz_2 = test_quizzes

    test_quiz_result_1: QuizResult = baker.make(
        QuizResult,
        company=test_company,
        user=test_user,
        quiz=test_quiz_1,
        status=UserQuizStatus.COMPLETED.value,
        score=2
    )

    test_quiz_result_2: QuizResult = baker.make(
        QuizResult,
        company=test_company,
        user=test_user,
        quiz=test_quiz_2,
        status=UserQuizStatus.COMPLETED.value,
        score=1
    )

    return test_quiz_result_1, test_quiz_result_2
