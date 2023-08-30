import configparser
from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class BotConfig:
    token: str
    admin_id: int


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig


def load_config(path: str) -> Config:
    config = configparser.ConfigParser()
    config.read(path)

    bot_config = config["bot"]

    return Config(
        bot=BotConfig(
            token=bot_config.get("token"),
            admin_id=bot_config.getint("admin_id"),
        ),
        db=DBConfig(**config["db"]),
    )
