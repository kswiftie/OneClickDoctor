from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from config import BOT_TOKEN, REDIS_URL


bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(storage=MemoryStorage())
storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)
