from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GITHUB_COPILOT_TOKEN: str = Field(default="")
    WEBSHARE_PROXY_USERNAME: str = Field(default="")
    WEBSHARE_PROXY_PASSWORD: str = Field(default="")
    WEBSHARE_PROXY_HOST: str = Field(default="")
    WEBSHARE_PROXY_PORT: int = Field(default=80)


    model_config = {
        "env_file": ".env",
    }


settings = Settings()
