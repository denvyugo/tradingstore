from sqlalchemy import Column, String, Integer, DECIMAL
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key = True)
    address = Column(String)
    price_km = Column(DECIMAL)
    title = Column(String)

    def __init__(self, address, price_km, title):
        self.address = address
        self.price_km = price_km
        self.title = title

    def __repr__(self):
        return f'<Store: {self.title}>'