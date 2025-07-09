import os
from pydantic import model_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")
load_dotenv(ENV_PATH)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.environ.get("ENV", "DEV")
    SITE_DOMAIN: str = "jungle_every_time"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    SECRET_KEY_AUTH: str = os.environ.get("SECRET_KEY_AUTH", "")
    DB_HOST: str = os.environ.get("DB_HOST", "")
    DB_USER: str = os.environ.get("DB_USER", "")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")
    DB_NAME: str = os.environ.get("DB_NAME", "")
    DB_URL: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

    STUN_SERVER_URL: str = os.environ.get(
        "STUN_SERVER_URL",
        "stun:stun.l.google.com:19302",
    )
    TURN_SERVER_URLS: list[str] = []
    TURN_SERVER_URL: str | None = os.environ.get("TURN_SERVER_URL")
    TURN_USERNAME: str | None = os.environ.get("TURN_USERNAME")
    TURN_PASSWORD: str | None = os.environ.get("TURN_PASSWORD")

    @model_validator(mode="after")
    def build_turn_server_list(self) -> "Settings":
        if not self.TURN_SERVER_URLS:
            env_value = os.environ.get("TURN_SERVER_URLS")
            if env_value:
                self.TURN_SERVER_URLS = [u.strip() for u in env_value.split(",") if u.strip()]
        if not self.TURN_SERVER_URLS and self.TURN_SERVER_URL:
            self.TURN_SERVER_URLS = [self.TURN_SERVER_URL]
        return self


settings = Settings()
