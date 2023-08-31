from aiogram import Dispatcher

from .dbmiddlewares import DBModelsMiddleware


def register_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.message.middleware.register(middleware=DBModelsMiddleware())
