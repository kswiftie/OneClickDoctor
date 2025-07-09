import asyncio
import logging

from bot import bot, dp
from routers.v1 import v1_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ]
)


async def main():
    dp.include_router(v1_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
