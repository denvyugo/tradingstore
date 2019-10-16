# импортируем специальные поля Алхимии для инициализации полей таблицы
from sqlalchemy import Column, Integer
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    chat_id = Column(Integer)
    role = Column(Integer)

    def __init__(self, chat_id, role):
        self.chat_id = chat_id
        self.role = role

    def __repr__(self):
        return f'<User: {self.id}, chat = {self.chat_id}>'
