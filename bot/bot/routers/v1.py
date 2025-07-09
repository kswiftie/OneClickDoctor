from aiogram import Router
from handlers.v1 import start, select_doctor, search, navigation

v1_router = Router()
v1_router.include_router(start.router)
v1_router.include_router(navigation.router)
v1_router.include_router(search.router)
v1_router.include_router(select_doctor.router)
