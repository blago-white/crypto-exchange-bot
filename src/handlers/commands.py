from aiogram.types import Message


async def start(message: Message) -> None:
    await message.reply(text="""Hello! This is bot!""")
