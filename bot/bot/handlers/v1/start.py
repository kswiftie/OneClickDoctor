from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import ChatState
from keyboards.inline import main_menu_kb

router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(ChatState.chatting)
    await state.update_data(messages=[])
    await message.answer(
        (
            '👋 *Привет!*\n\n'
            '*Я помогу тебе с подбором врача.*\n\n'
            'Если ты уже знаешь, какой специалист тебе нужен — '
            'воспользуйся кнопкой _"Подобрать врача"._\n'
            'А если *пока не уверен(а)*, какой врач подходит — '
            'опиши свои симптомы, и я помогу разобраться. 💬'
        ),
        parse_mode='Markdown',
        reply_markup=main_menu_kb()
    )
