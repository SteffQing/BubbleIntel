import asyncio
from aiogram import Bot, Dispatcher

from services.httpx import close_client, init_client
from utils.logger import Logger
from utils.config import BOT_TOKEN, BOT_NAME

from handlers import common


if BOT_TOKEN is None:
    raise Exception("BOT_TOKEN is not defined")
if BOT_NAME is None:
    raise Exception("BOT_NAME is not defined")

log = Logger(BOT_NAME)
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
