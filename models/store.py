# импортируем модуль инициализации декларативного класса Алхимии
from sqlalchemy import Column, Float, String, Integer
from DB.dbcore import Base


class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key = True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    price_km = Column(Float)
    title = Column(String)

    def __init__(self, address, latitude, longitude, price_km, title):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.price_km = price_km
        self.title = title

    def __repr__(self):
        return f'<Store: {self.title}>'