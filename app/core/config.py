from decouple import Config, RepositoryEnv
import os

env = Config(RepositoryEnv(f"{os.path.abspath(os.path.dirname(__name__))}/.env"))


class Settings:
    def __init__(self):
        self.STORAGE_TYPE: str = env.get("STORAGE_TYPE", "json")
        self.JSON_DB_FILE: str = env.get("JSON_DB_FILE", "db.json")
        self.DB_CONNECTION_DRIVER: str = env.get("DB_CONNECTION_DRIVER", "postgresql")
        self.DB_HOST = env.get("DB_HOST", "127.0.0.1")
        self.DB_NAME: str = env.get("DB_NAME", "pysoap")
        self.DB_USER: str = env.get("DB_USER", "postgres")
        self.DB_PASS: str = env.get("DB_PASS", "postgres")


settings = Settings()
