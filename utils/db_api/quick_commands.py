from utils.db_api.schemas.user import User
from utils.db_api.db_gino import db

from asyncpg import UniqueViolationError

form_dict = {
            "ПССМП": "pssmp",
            "Номер бригады": "brigade_number",
            "Номер карты вызова": "call_card_number",
            "Адрес места вызова": "call_address",
            "Пол и возраст больного": "patient_gender_age",
            "Диагноз основной": "main_diagnosis",
            "Общая тяжесть состояния": "condition_severity",
            "Уровень сознания по ШКГ": "consciousness_level",
            "ЧСС": "hr",
            "АД": "bp",
            "ЧДД": "rr",
            "SpO2": "spo",
            "Температура тела": "body_temperature",
            "Прописка": "registration",
            "Телефон бригады": "brigade_phone"
        }

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
        global form_dict
        form=''
        for key, value in form_dict.items():
            if point in key:
                form+=f"<b>> {key}: {getattr(user, value)}</b>" + '\n'
            else:
                form+=f"{key}: {getattr(user, value)}" + '\n'
            if getattr(user, value):
                form+=f"✅ {key}: {getattr(user, value)}" + '\n'
        return form
    except Exception:
        return None


