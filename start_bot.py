import asyncio
import logging
import os

from aiogram import Router
from aiogram import Bot
from heandlers import dp
TOKEN = os.getenv("TOKEN")


async def main():
    router = Router()
    bot = Bot(TOKEN)
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message"])


if __name__ == '__main__':
    asyncio.run(main())
