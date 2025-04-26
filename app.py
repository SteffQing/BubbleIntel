import asyncio
from aiogram import Bot, Dispatcher

from services.httpx import close_client, init_client
from utils.logger import Logger
from utils.config import BOT_TOKEN

from handlers import common


if BOT_TOKEN is None:
    raise Exception("BOT_TOKEN is not defined")

log = Logger("Bubble Intel Bot")
log.debug("Bot is loading")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    await init_client()
    try:
        log.debug("Bot initializing.")
        
        await common.set_bot_commands(bot)
        
        dp.include_routers(
            common.router,
        )
        
        log.debug("Bot commands and routers loaded.")
        
        await dp.start_polling(bot)
    finally:
        await close_client()

    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
