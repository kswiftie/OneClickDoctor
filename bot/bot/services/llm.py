async def get_llm_answer(messages: list[dict]) -> str:
    user_input = messages[-1]['content']
    return f'Ты сказал: {user_input}'
