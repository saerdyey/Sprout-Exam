from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "thisIsSecretKey"
    admin_username: str = "admin"
    admin_password: str = "password"
    pgdb_host: str = "localhost"
    pgdb_port: str = "5432"
    pgdb_username: str = "postgres"
    pgdb_password: str = "password123"
    pgdb_name: str = "sprout_exam"


    class Config:
        env_file = ".env"