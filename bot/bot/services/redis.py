import redis
from pprint import pprint

# Подключение к Redis
r = redis.Redis(
    host='localhost',
    port=6380,
    password='redis',
    decode_responses=True
)

# Получить все ключи, связанные с FSM
keys = r.keys("fsm*")
pprint(keys)

# Пример: получить состояние пользователя
for key in keys:
    value = r.get(key)
    pprint(f"{key}: {value}")