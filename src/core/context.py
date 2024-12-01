from concurrent.futures import ThreadPoolExecutor
from src.core.db import create_database
from src.core import settings
from fastapi.security import OAuth2PasswordBearer


class Context:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = create_database(settings.database_url)
            cls._instance.executor = ThreadPoolExecutor()
        return cls._instance


context = Context()
