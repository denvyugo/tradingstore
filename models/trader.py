# импортируем специальные поля Алхимии для инициализации полей таблицы
from sqlalchemy import Column, String, Integer
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base


class Trader(Base):
    __tablename__ = 'traders'
    id = Column(Integer, primary_key = True)
    chat_id = Column(String)
    phone = Column(String)
    user_name = Column(String)

    def __init__(self, chat_id, phone, user_name):
        self.chat_id = chat_id
        self.phone = phone
        self.user_name = user_name

    def __repr__(self):
        return f'<Trader: {self.__tablename__}'