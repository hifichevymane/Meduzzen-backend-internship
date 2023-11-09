from pydantic import BaseModel


class UserRequestUpdateStatusBody(BaseModel):
    status: str


class UserRequestBody(BaseModel):
    company: int
