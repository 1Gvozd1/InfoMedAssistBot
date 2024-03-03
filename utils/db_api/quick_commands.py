from utils.db_api.schemas.user import User
from utils.db_api.db_gino import db

from asyncpg import UniqueViolationError

async def add_user(user_id: int, first_name: str, last_name: str, username: str, status: str):
    try:
        user = User(user_id = user_id, first_name = first_name, last_name = last_name, username = username, status = status)
        await user.create()
    except UniqueViolationError:
        print("Пользователь не добавлен")

async def select_all_users():
    users = await User.query.gino.all()
    return users

async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count

async def get_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user

async def update_user_name(user_id, new_name):
    user = await get_user(user_id)
    await user.update(update_name = new_name).apply()