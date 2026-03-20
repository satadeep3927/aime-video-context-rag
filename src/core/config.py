from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GITHUB_COPILOT_TOKEN: str = Field(default="")

    model_config = {
        "env_file": ".env",
    }


settings = Settings()
