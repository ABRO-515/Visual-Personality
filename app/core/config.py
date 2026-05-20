from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Visual Personality API"
    API_VERSION: str = "0.1.0"

    ALLOWED_ORIGINS: list[str] = ["*"]

    MIN_IMAGE_WIDTH: int = 300
    MIN_IMAGE_HEIGHT: int = 300
    BLUR_THRESHOLD: float = 80.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
