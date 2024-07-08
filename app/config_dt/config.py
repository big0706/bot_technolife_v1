import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    database_url: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config() -> Config:
    load_dotenv()
    return Config(tg_bot=TgBot(os.getenv('BOT_TOKEN')), db=DatabaseConfig(os.getenv('SQLALCHEMY_URL')))
