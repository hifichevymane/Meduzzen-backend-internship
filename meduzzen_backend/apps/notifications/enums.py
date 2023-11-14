from enum import StrEnum, auto


class NotificationStatus(StrEnum):
    UNREAD = auto()
    READ = auto()

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
