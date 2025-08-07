from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    database_url: str = "sqlite:///./tenders.db"
    description: str = ""
    project_name: str
    project_host: str
    project_port: int


    model_config = SettingsConfigDict(env_nested_delimiter="__")





if __name__ == "__main__":
    cfg: Config = Config()

    print(BASE_DIR, cfg.database_url,)
    print(cfg.project_name)
    print(cfg.project_host)
    print(cfg.project_port)