from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from states import ChatState
from services import llm

router = Router()


@router.message(ChatState.chatting)
async def chat_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get('messages', [])

    messages.append({'role': 'user', 'content': message.text})
    assistant_reply = await llm.get_llm_answer(messages)
    messages.append({'role': 'assistant', 'content': assistant_reply})

    await state.update_data(messages=messages)
    await message.answer(assistant_reply)
