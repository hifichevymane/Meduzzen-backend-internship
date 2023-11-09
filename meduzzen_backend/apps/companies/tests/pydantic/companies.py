from pydantic import BaseModel


class CompanyInviteBody(BaseModel):
    user: int
    company: int


class CompanyInviteUpdateStatusBody(BaseModel):
    status: str


class CompanyMemberChangeRoleBody(BaseModel):
    role: str


class CompanyMemberRatingBody(BaseModel):
    company: int
    user: int
