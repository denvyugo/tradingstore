# импортируем специальные поля Алхимии для инициализации полей таблицы
from sqlalchemy import Column, String, Integer
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key = True)
    address = Column(String)
    chat_id = Column(Integer)
    email = Column(String)
    phone = Column(String)
    user_name = Column(String)

    def __init__(self, address, chat_id, phone, user_name):
        self.address = address
        self.chat_id = chat_id
        self.phone = phone
        self.user_name = user_name

    def __repr__(self):
        return f'<Client: {self.id}>'