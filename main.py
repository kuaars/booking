import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from handlers.admin import router as admin_router
from handlers.user import router as user_router


async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(admin_router)
    dispatcher.include_router(user_router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
