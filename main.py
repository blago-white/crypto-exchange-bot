import asyncio
import logging

import src
from src.config import settings, config


async def main() -> None:
    _start_logger()

    await src.setup_bot(
        config=config.load_config(path=settings.CONFIG_FILE)
    )


def _start_logger() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)s) - %(message)s"
    )


if __name__ == '__main__':
    asyncio.run(main())
