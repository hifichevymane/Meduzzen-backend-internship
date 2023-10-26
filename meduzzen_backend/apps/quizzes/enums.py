from enum import StrEnum, auto


# Status of passing quizes
class UserQuizStatus(StrEnum):
    PENDING = auto()
    COMPLETED = auto()

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
