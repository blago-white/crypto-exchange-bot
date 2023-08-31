import configparser
from dataclasses import dataclass

from src.utils import objects


@dataclass(frozen=True)
class DBConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass(frozen=True)
class BotConfig:
    token: str
    admin_id: int


@dataclass(frozen=True)
class AppConfig(metaclass=objects.BaseSimpleObject):
    bot: BotConfig
    db: DBConfig


def load_config(path: str) -> AppConfig:
    config = configparser.ConfigParser()
    config.read(path)

    bot_config = config["bot"]

    return AppConfig(
        bot=BotConfig(
            token=bot_config.get("token"),
            admin_id=bot_config.getint("admin_id"),
        ),
        db=DBConfig(**config["db"]),
    )
