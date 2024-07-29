import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config_dt.config import Config, load_config
from app.handlers import (command_handler, admin_handler, manager_handler, stuff_handler, other_handler)
from app.models.models import async_main

logging.basicConfig(level=logging.INFO,
                    format='{filename}:{lineno} #{levelname:<8}'
                           '[{asctime}] - {name} - {message}',
                    style='{')

logger = logging.getLogger(__name__)


async def main():

    logger.info('Starting bot')

    config: Config = load_config()

    await async_main()

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(command_handler.router,
                       admin_handler.router,
                       manager_handler.router,
                       stuff_handler.router,
                       other_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Interrupted by admin')
