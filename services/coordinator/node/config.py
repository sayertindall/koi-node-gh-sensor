from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)

    # Optional: Add computed property for base_url if needed frequently
    # @property
    # def BASE_URL(self) -> str:
    #     return f"http://{self.HOST}:{self.PORT}/koi-net"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
