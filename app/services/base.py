from app.utils.db_manager import DBManager


class BaseService:
    """Базовый класс, использующий DBManager для взаимодействия с репозиторием"""
    db: DBManager | None

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db