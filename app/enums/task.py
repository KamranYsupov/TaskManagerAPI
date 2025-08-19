import enum


class TaskStatus(str, enum.Enum):
    CREATED = 'Cоздано'
    IN_PROGRESS = 'В работе'
    COMPLETED = 'Завершено'