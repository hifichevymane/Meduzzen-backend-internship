from typing import List

from pydantic import BaseModel


class AnswerOptionRequestBodySchema(BaseModel):
    text: str


class QuestionRequestBodySchema(BaseModel):
    text: str
    options: List[int] # List of options' ids
    answer: List[int] # List of answer' ids


class QuizRequestBodySchema(BaseModel):
    title: str
    company: int # Company id
    description: str
    questions: List[int] # List of questions' ids


class QuizResultRequestBodySchema(BaseModel):
    quiz: int # Quiz id


class UserAnswerRequestBodySchema(BaseModel):
    quiz: int # Quiz id
    question: int # Question id
    answer: List[int] # List of answers' ids
    quiz_result: int # Quiz result id
