from typing import List

from pydantic import BaseModel


class AnswerOptionBody(BaseModel):
    text: str


class QuestionBody(BaseModel):
    text: str
    options: List[int]
    answer: List[int]


class QuizBody(BaseModel):
    title: str
    company: int
    description: str
    questions: List[int]


class QuizResultBody(BaseModel):
    quiz: int


class UserAnswerBody(BaseModel):
    quiz: int
    question: int
    answer: List[int]
    quiz_result: int
