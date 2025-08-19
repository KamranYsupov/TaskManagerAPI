from dependency_injector import containers, providers

from app.db import DataBaseManager
from app.core.config import settings
from app.db.models import Task
from app.repositories import RepositoryTask
from app.services import TaskService


class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_task = providers.Factory(
        RepositoryTask, model=Task, session=session
    )
    # endregion

    # region services
    task_service = providers.Factory(
        TaskService,
        repository=repository_task,
        unique_fields=('name', )
    )

    # endregion



