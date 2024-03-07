from utils.db_api.schemas.user import User
from utils.db_api.db_gino import db

from asyncpg import UniqueViolationError

async def add_user(user_id: int, first_name: str, last_name: str, username: str, status: str):
    try:
        user = User(user_id = user_id, first_name = first_name, last_name = last_name, username = username, status = status)
        await user.create()
    except UniqueViolationError:
        print("Пользователь не добавлен")

async def get_all_users():
    users = await User.query.gino.all()
    return users

async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count

async def get_user(user_id):
    try:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user
    except Exception:
        return None

async def update_user_name(user_id, new_name):
    user = await get_user(user_id)
    await user.update(update_name = new_name).apply()

async def get_form(user_id, point):
    try:
        user = await get_user(user_id)
        form = f"""\
{'<b>' if point == "ПССМП" else ''}ПССМП: {user.first_name}{'</b>' if point == "ПССМП" else ''}
Номер бригады:
Номер карты вызова:
Адрес места вызова:
Пол и возраст больного:
Диагноз основной:
Общая тяжесть состояния:
Уровень сознания по ШКГ:
ЧСС:
АД:
ЧДД:
SpO2:
Температура тела:
Прописка:
Телефон бригады:
Запрос на госпитализацию
"""
        return form
    except Exception:
        return None