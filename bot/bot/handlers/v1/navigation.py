from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from states import ChatState
from keyboards.inline import main_menu_kb, menu_button

router = Router()


@router.callback_query(lambda c: c.data.startswith('to_menu'))
async def to_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data in [
        'to_menu_from_info',
        'to_menu_from_doctor_search'
    ]:
        await callback.message.delete()
    else:
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
    await state.clear()
    await callback.message.answer(
        '👋 *Главное меню*\n\nПожалуйста, выберите действие:',
        parse_mode='Markdown',
        reply_markup=main_menu_kb()
    )


@router.callback_query(lambda c: c.data == 'chat')
async def chat_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.answer()
    await state.clear()
    await state.set_state(ChatState.chatting)
    await state.update_data(messages=[])

    await callback.message.delete()
    await callback.message.answer(
        '💬 Опишите ваши симптомы, и я помогу определить, '
        'к какому врачу обратиться.'
    )


@router.callback_query(lambda c: c.data == 'info')
async def info_callback_handler(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    await callback.message.delete()
    msg = (
        'ℹ️ *OneClickDoctor* — бот для подбора врача и помощи с '
        'симптомами.\n\n'
        '• Быстрый подбор врача по специализации\n'
        '• Помощь с определением, к какому врачу обратиться по симптомам\n\n'
        'Разработчик: @yourusername'
    )
    await callback.message.answer(
        msg,
        parse_mode='Markdown',
        reply_markup=menu_button(from_info=True)
    ) 