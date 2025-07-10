import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION: str = os.getenv("VERSION")
    DEBUG: bool = os.getenv("DEBUG")
    CORS_ALLOWED_ORIGINS: str = os.getenv("CORS_ALLOWED_ORIGINS")

    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: int = os.getenv("POSTGRES_PORT")
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_DRIVER: str = os.getenv("POSTGRES_DRIVER")
    DB_NAME: str = os.getenv("POSTGRES_DB")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ENCODE_ALGORITHM: str = os.getenv("JWT_ENCODE_ALGORITHM")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_SECRET_KEY: str = os.getenv("GOOGLE_SECRET_KEY")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_TOKEN_URL: str = os.getenv("GOOGLE_TOKEN_URL")
    GOOGLE_USER_INFO_URL: str = os.getenv("GOOGLE_USER_INFO_URL")

    YANDEX_CLIENT_ID: str = os.getenv("YANDEX_CLIENT_ID")
    YANDEX_SECRET_KEY: str = os.getenv("YANDEX_SECRET_KEY")
    YANDEX_REDIRECT_URI: str = os.getenv("YANDEX_REDIRECT_URI")
    YANDEX_TOKEN_URL: str = os.getenv("YANDEX_TOKEN_URL")
    YANDEX_USER_INFO_URL: str = os.getenv("YANDEX_USER_INFO_URL")

    PROFILE_MICROSERVICE_BASE_URL: str = os.getenv("PROFILE_MICROSERVICE_BASE_URL")
    PROFILE_MICROSERVICE_USER_PROFILE_ENDPOINT: str = os.getenv(
        "PROFILE_MICROSERVICE_USER_PROFILE_ENDPOINT"
    )
    PROFILE_MICROSERVICE_USER_PROFILE_LIST_ENDPOINT: str = os.getenv(
        "PROFILE_MICROSERVICE_USER_PROFILE_LIST_ENDPOINT"
    )

    PHOTO_MICROSERVICE_BASE_URL: str = os.getenv("PHOTO_MICROSERVICE_BASE_URL")
    PHOTO_MICROSERVICE_PHOTO_ENDPOINT: str = os.getenv(
        "PHOTO_MICROSERVICE_PHOTO_ENDPOINT"
    )
    PHOTO_MICROSERVICE_LIST_OWN_PHOTOS_ENDPOINT: str = os.getenv(
        "PHOTO_MICROSERVICE_LIST_OWN_PHOTOS_ENDPOINT"
    )
    PHOTO_MICROSERVICE_LIST_USERS_PHOTOS_ENDPOINT: str = os.getenv(
        "PHOTO_MICROSERVICE_LIST_USERS_PHOTOS_ENDPOINT"
    )

    SWIPE_MICROSERVICE_BASE_URL: str = os.getenv("SWIPE_MICROSERVICE_BASE_URL")
    PROCESS_SWIPES_TOPIC: str = os.getenv("PROCESS_SWIPES_TOPIC")
    EVENT_TYPE_PROCESS_SWIPES: str = os.getenv("EVENT_TYPE_PROCESS_SWIPES")
    KAFKA_BROKER_ADDRESS: str = os.getenv("KAFKA_BROKER_ADDRESS")

    @property
    def db_url(self):
        return (
            f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def google_redirect_url(self):
        return (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code"
            f"&client_id={self.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={self.GOOGLE_REDIRECT_URI}"
            f"&scope=openid%20profile%20email&access_type=offline"
        )

    @property
    def yandex_redirect_url(self) -> str:
        return (
            f"https://oauth.yandex.ru/authorize?response_type=code&client_id"
            f"={self.YANDEX_CLIENT_ID}&force_confirm=yes"
        )
