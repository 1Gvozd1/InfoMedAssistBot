from gino import Gino
from typing import List
import sqlalchemy as sa
from sqlalchemy import Column, BigInteger,String
import datetime
import os


from aiogram import Dispatcher

db = Gino()

ip = 'localhost'
PGUSER = 'postgres'
PGPASSWORD = 'd6435h7j7d34'
DATABASE = 'gino'

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
    )

async def on_startup(dispatcher: Dispatcher):
    print('Установка связи с PostgreSQL')
    await db.set_bind(POSTGRES_URI)