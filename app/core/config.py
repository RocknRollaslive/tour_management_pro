from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Tour Management Pro"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    sqlite_db_file: str = "tour_master.db"


settings = Settings()
