from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states import ChatState

router = Router()

CITIES = [
    'Санкт-Петербург',
    'Москва'
]

# @router.callback_query(lambda c: c.data == 'find_doctor')
# async def city_select_handler(
#     callback: types.CallbackQuery,
#     state: FSMContext
# ):
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(
#                 text=city,
#                 callback_data=f'city_{city}')]
#             for city in CITIES
#         ]
#     )
#     await callback.message.answer('Выберите город:', reply_markup=keyboard)
#     await callback.answer()
#     await state.set_state(ChatState.chatting)


async def show_city_selection(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=city, callback_data=f'city_{city}')]
            for city in CITIES
        ]
    )
    await message.answer('Выберите город:', reply_markup=keyboard)
    await state.set_state(ChatState.chatting)


@router.callback_query(F.data == 'find_doctor')
async def find_doctor_callback(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await show_city_selection(callback.message, state)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('city_'))
async def ask_about_doctor_handler(
    callback: types.CallbackQuery,
    state: FSMContext
):
    city = callback.data.replace('city_', '')
    await callback.message.delete()
    await callback.message.answer(
        f'Вы выбрали город: {city}.\n\n'
        'Знаете ли вы, какого врача ищете?',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text='Да', callback_data='doctor_known'),
                 InlineKeyboardButton(
                     text='Нет', callback_data='doctor_unknown')]
            ]
        )
    )
    await callback.answer()
    await state.set_state(ChatState.chatting)


@router.callback_query(lambda c: c.data == 'doctor_known')
async def doctor_known_handler(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Отлично! Укажите, какого врача вы ищете.')
    await state.set_state(ChatState.chatting)


@router.callback_query(lambda c: c.data == 'doctor_unknown')
async def doctor_unknown_handler(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        'Хорошо, я помогу подобрать врача по вашим симптомам.'
    )
    await state.set_state(ChatState.chatting)
