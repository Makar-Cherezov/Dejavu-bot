import bot_secrets
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode


import asyncio
from handlers import router



async def main():
    bot = Bot(token=bot_secrets.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(filename="BotLogs",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.ERROR)
    asyncio.run(main())
