from pydantic import BaseModel

from users.enums import UsersRequestStatus


class UserModelSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


class UserRequestUpdateStatusBodySchema(BaseModel):
    status: UsersRequestStatus


class UserRequestBodySchema(BaseModel):
    company: int # Company id