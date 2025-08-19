from .base import CRUDBaseService
from app.repositories.task import RepositoryTask


class TaskService(CRUDBaseService[RepositoryTask]):
    """Сервис для RepositoryTask"""
    pass