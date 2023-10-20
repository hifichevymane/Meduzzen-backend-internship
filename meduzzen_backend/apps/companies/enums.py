from enum import StrEnum, auto


# Status choices for CompanyInvitations model
class CompanyInvitationStatus(StrEnum):
    PENDING = auto()
    ACCEPTED = auto()
    DECLINED = auto()
    REVOKED = auto()

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


# Visibility choices 
class Visibility(StrEnum):
    VISIBLE = auto()
    HIDDEN = auto()

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


# Company member role in Company
class CompanyMemberRole(StrEnum):
    ADMIN = auto()
    COMMON = auto()

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
