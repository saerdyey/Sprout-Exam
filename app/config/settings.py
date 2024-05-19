from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "thisIsSecretKey"
    admin_username: str = "admin"
    admin_password: str = "password"

    class Config:
        env_file = ".env"