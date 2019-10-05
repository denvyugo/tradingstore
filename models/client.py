# импортируем специальные поля Алхимии для инициализации полей таблицы
from sqlalchemy import Column, Float, String, Integer
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key = True)
    address = Column(String)
    chat_id = Column(Integer)
    email = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String)
    title = Column(String)
    user_name = Column(String)

    def __init__(self, address, chat_id, email, latitude, longitude, phone, title, user_name):
        self.address = address
        self.chat_id = chat_id
        self.email = email
        self.latitude = latitude
        self.longitude = longitude
        self.phone = phone
        self.title = title
        self.user_name = user_name

    def __repr__(self):
        return f'<Client: {self.id}, {self.title}, {self.address}>'