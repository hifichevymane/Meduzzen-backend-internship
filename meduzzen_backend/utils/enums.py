from enum import StrEnum, auto


class ExportDataFileType(StrEnum):
    CSV = auto()
    JSON = auto()

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
