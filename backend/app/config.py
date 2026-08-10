from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-luna"


    # Database
    database_url: str = "sqlite:///./data/app.db"

    # Turso
    turso_database_url: str = ""
    turso_auth_token: str = ""
    
    # Frontend access
    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )


    # Teacher protection
    teacher_access_code: str = "change-this-code"


    # Automatic deletion
    delete_after_days: int = 7


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings():

    settings = Settings()

    print("KEY LOADED:", settings.openai_api_key[:10])

    return settings