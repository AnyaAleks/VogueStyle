import logging
from os import getenv
from asyncio import run
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from routers import start_router, new_user_router, enter_user_router

session = AiohttpSession()
bot = Bot(token=getenv("BOT_TOKEN"), session=session, storage=MemoryStorage())
dp = Dispatcher()

async def main() -> None:
    dp.include_router(start_router)
    dp.include_router(enter_user_router)
    dp.include_router(new_user_router)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run(main())