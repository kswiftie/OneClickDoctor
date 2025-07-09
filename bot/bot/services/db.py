async def get_doctors_by_city_and_specialty(city: str, specialty: str) -> str:
    return (
        f'🔎 В городе {city} найдено 5 врачей по специализации "{specialty}".'
    )