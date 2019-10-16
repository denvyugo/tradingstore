# импортируем специальные поля Алхимии для инициализации полей таблицы
from sqlalchemy import Column, DateTime, Float, Boolean, Integer, ForeignKey
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base
# импортируем модель продуктов для связки моделей
from models.client import Client
from models.store import Store
from models.trader import Trader


class OrderInfo(Base):
    __tablename__ = 'order_info'
    id = Column(Integer, primary_key = True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    delivery_cost = Column(Float)
    is_current = Column(Boolean)
    order_date = Column(DateTime)
    status = Column(Integer)
    store_id = Column(Integer, ForeignKey('stores.id'))
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
    store = relationship(
        Store,
        backref=backref('order_info',
                        uselist=True,
                        cascade='delete,all'))

    def __init__(self, client_id, delivery_cost, is_current, order_date, status, store_id, trader_id):
        self.client_id = client_id
        self.delivery_cost = delivery_cost
        self.is_current = is_current
        self.order_date = order_date
        self.status = status
        self.store_id = store_id
        self.trader_id = trader_id

    def __repr__(self):
        return f'<OrderInfo: {self.id}, {self.order_date}, {self.client_id}, {self.trader_id}>'

    def __str__(self):
        return f'OderID: {self.id} of {self.order_date} for {self.client_id}'
