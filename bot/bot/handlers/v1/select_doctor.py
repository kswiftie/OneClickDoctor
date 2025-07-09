from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from states import ChatState
from services import llm
from keyboards.inline import menu_button

router = Router()


@router.message(ChatState.chatting)
async def chat_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get('messages', [])
    messages.append({'role': 'user', 'content': message.text})
    # assistant_reply = await llm.generate_answer(messages)
    assistant_reply = 'ждем...'
    messages.append({'role': 'assistant', 'content': assistant_reply})
    await state.update_data(messages=messages)
    await message.answer(assistant_reply, reply_markup=menu_button())
