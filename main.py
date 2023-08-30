import asyncio
import logging

import src
from src.config import settings

CONFIG_FILE = "botconfig.ini"


async def main() -> None:
    _start_logger()

    await src.setup_bot(
        config=src.config.settings.load_config(path=CONFIG_FILE)
    )


def _start_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)s) - %(message)s"
    )


if __name__ == '__main__':
    asyncio.run(main())
