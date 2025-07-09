from aiogram import Router
from handlers.v1 import commands, chat, doctor

v1_router = Router()
v1_router.include_router(commands.router)
v1_router.include_router(doctor.router)
v1_router.include_router(chat.router)
