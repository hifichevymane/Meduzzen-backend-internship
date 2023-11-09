from pydantic import BaseModel

from users.enums import UsersRequestStatus


class UserRequestUpdateStatusBodySchema(BaseModel):
    status: UsersRequestStatus


class UserRequestBodySchema(BaseModel):
    company: int # Company id