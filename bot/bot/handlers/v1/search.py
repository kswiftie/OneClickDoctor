from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from states import DoctorSearch
from services.db import get_doctors_by_city_and_specialty
from keyboards.inline import (
    get_city_keyboard, get_specialty_keyboard, menu_button
)

router = Router()


@router.callback_query(lambda c: c.data == 'find_doctor')
async def find_doctor_callback(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    await state.clear()
    await state.set_state(DoctorSearch.city)
    await callback.message.delete()
    await callback.message.answer(
        '🌆 Выберите город:',
        reply_markup=get_city_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith('doctor_city_'))
async def doctor_city_chosen(callback: types.CallbackQuery, state: FSMContext):
    city = callback.data.replace('doctor_city_', '')
    await state.update_data(city=city)
    await state.set_state(DoctorSearch.specialty)
    await callback.message.delete()
    await callback.message.answer(
        f'🌆 Выбран город: {city} \n\n🏥 Выберите специализацию: ',
        reply_markup=get_specialty_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith('doctor_spec_'))
async def doctor_specialty_chosen(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    specialty = callback.data.replace('doctor_spec_', '')
    data = await state.get_data()
    city = data.get('city', '—')
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        f'🌆 Город: {city}\n\n🏥 Специализация: {specialty}'
    )
    await callback.message.answer(
        await get_doctors_by_city_and_specialty(city, specialty),
        reply_markup=menu_button()
    )
