from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GITHUB_COPILOT_TOKEN: str = Field(default="")
    WEBSHARE_PROXY_USERNAME: str = Field(default="")
    WEBSHARE_PROXY_PASSWORD: str = Field(default="")


    model_config = {
        "env_file": ".env",
    }


settings = Settings()
