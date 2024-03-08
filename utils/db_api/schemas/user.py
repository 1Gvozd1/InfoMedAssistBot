from sqlalchemy import Column,BigInteger,String,SmallInteger,Integer,Float,sql

from utils.db_api.db_gino import TimedBaseModel

class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key = True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(50))
    status = Column(String(30))
    pssmp = Column(String(50)) # ПССМП
    brigade_number = Column(String(25)) # Номер бригады
    call_card_number = Column(String(10)) # Номер карты вызова
    call_address = Column(String(200)) # Адрес места вызова
    patient_gender_age = Column(String(25)) # Пол и возраст больного
    main_diagnosis = Column(String(1000)) # Диагноз основной
    condition_severity = Column(String(25)) # Общая тяжесть состояния
    consciousness_level = Column(String(5)) # Уровень сознания по ШКГ
    hr = Column(String(10)) # ЧСС
    bp = Column(String(25)) # АД
    rr = Column(String(5)) # ЧДД
    spo = Column(String(10)) # SPO2
    body_temperature = Column(String(10)) # Температура тела
    registration = Column(String(200)) # Прописка
    brigade_phone = Column(String(50)) # Телефон для связи с Бригадой

    query: sql.select