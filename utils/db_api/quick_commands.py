from utils.db_api.schemas.user import User
from utils.db_api.db_gino import db

from asyncpg import UniqueViolationError

async def add_user(user_id: int, 
                   first_name: str, 
                   last_name: str, 
                   username: str, 
                   status: str, 
                   pssmp: str, 
                   brigade_number: str, 
                   call_card_number: str, 
                   call_address: str,
                   patient_gender_age: str,
                   main_diagnosis: str,
                   condition_severity: str,
                   consciousness_level: str,
                   hr: str,
                   bp: str,
                   rr: str,
                   spo: str,
                   body_temperature: str,
                   registration: str,
                   brigade_phone: str
                   ):
    try:
        user = User(user_id = user_id, 
                    first_name = first_name, 
                    last_name = last_name, 
                    username = username, 
                    status = status, 
                    pssmp = pssmp, 
                    brigade_number = brigade_number,
                    call_card_number = call_card_number, 
                    call_address = call_address, 
                    patient_gender_age = patient_gender_age, 
                    main_diagnosis = main_diagnosis, 
                    condition_severity = condition_severity, 
                    consciousness_level = consciousness_level,
                    hr = hr,
                    bp = bp,
                    rr = rr,
                    spo = spo,
                    body_temperature = body_temperature,
                    registration = registration,
                    brigade_phone = brigade_phone,  
                    )
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
        form_lines = [
            f"ПССМП: {user.pssmp}",
            f"Номер бригады: {user.brigade_number}",
            f"Номер карты вызова: {user.call_card_number}",
            f"Адрес места вызова: {user.call_address}",
            f"Пол и возраст больного: {user.patient_gender_age}",
            f"Диагноз основной: {user.main_diagnosis}",
            f"Общая тяжесть состояния: {user.condition_severity}",
            f"Уровень сознания по ШКГ: {user.consciousness_level}",
            f"ЧСС: {user.hr}",
            f"АД: {user.bp}",
            f"ЧДД: {user.rr}",
            f"SpO2: {user.spo}",
            f"Температура тела: {user.body_temperature}",
            f"Прописка: {user.registration}",
            f"Телефон бригады: {user.brigade_phone}"
        ]
        # Формирование многострочной строки с выделением тегами <>
        form = "\n".join((f"<b>> {line} </b>") if point in line else (f"{line}") for line in form_lines)
        return form
    except Exception:
        return None


