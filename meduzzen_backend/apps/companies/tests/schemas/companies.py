from pydantic import BaseModel

from companies.enums import CompanyInvitationStatus, CompanyMemberRole


class CompanyInviteRequestBodySchema(BaseModel):
    user: int # User id
    company: int # Company id


class CompanyInviteUpdateStatusRequestBodySchema(BaseModel):
    status: CompanyInvitationStatus 


class CompanyMemberChangeRoleRequestBodySchema(BaseModel):
    role: CompanyMemberRole


class CompanyMemberRatingRequestBodySchema(BaseModel):
    company: int # Company id
    user: int # User id
