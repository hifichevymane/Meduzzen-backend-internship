from enum import StrEnum, auto


# Status choices for UsersRequests models
class UsersRequestStatus(StrEnum):
    PENDING = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    CANCELED = auto()

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
