import httpx


async def generate_answer(messages: list[dict]) -> str:
    payload = {
        'prompt': messages[-1]['content'],
        'max_length': 64,
        'temperature': 0.8,
        'top_p': 0.95
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            'http://localhost:8000/generate/',
            json=payload
        )
        response.raise_for_status()
        return response.json()['generated_text']
