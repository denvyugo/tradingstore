# импортируем специальные поля Алхимии для инициализации полей таблицы
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base
# импортируем модель продуктов для связки моделей
from models.client import Client
from models.trader import Trader


class OrderInfo(Base):
    __tablename__ = 'order_info'
    id = Column(Integer, primary_key = True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    order_date = Column(DateTime)
    status = Column(String)
    trader_id = Column(Integer, ForeignKey('traders.id'))
    # используется cascade='delete,all' для каскадного удаления данных ис таблицы
    client = relationship(
        Client,
        backref=backref('order_info',
                        uselist=True,
                        cascade='delete,all'))
    trader = relationship(
        Trader,
        backref=backref('order_info',
                        uselist=True,
                        cascade='delete,all'))

    def __init__(self, client_id, order_date, status, trader_id):
        self.client_id = client_id
        self.order_date = order_date
        self.status = status
        self.trader_id = trader_id

    def __repr__(self):
        return f'<OrderInfo: {self.__tablename__}'