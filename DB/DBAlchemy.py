import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import config
from settings import utility

from DB.dbcore import Base

from models.category import Category
from models.client import Client
from models.order import Order
from models.order_info import OrderInfo
from models.product import Products
from models.store import Store
from models.user import User


class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного и только один экземпляра объекта,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сесии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        self.__session = sessionmaker(bind=self.engine)
        self._session = self.__session()
        if not os.path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)
            self._set_tabs()

    def _set_tabs(self):
        """
        Метод заполнения полей таблицы Тест
        """
        category_1 = Category(name='Полуфабрикаты', is_active=True)
        category_2 = Category(name='Бакалея', is_active=True)
        category_3 = Category(name='Мороженое', is_active=True)

        product_1 = Products(name='Вареники(Фирменные)', title='ТМ Геркулес 400 гр',
                             price=542.01, quantity=12, is_active=True, category=category_1)
        product_2 = Products(name='Пельмени(Домашние)', title='ТМ Вкуснотеево 450 гр',
                             price=322.5, quantity=23, is_active=True, category=category_1)
        product_3 = Products(name='Колбаса(Докторская)', title='ТМ Доброе 500 гр',
                             price=420, quantity=15, is_active=True, category=category_2)
        product_4 = Products(name='Сосиски(Молочные)', title='ТМ Веселые 700 гр',
                             price=312.56, quantity=36, is_active=True, category=category_2)
        product_5 = Products(name='Пьяная вишня', title='ТМ Молочный берег 50 гр',
                             price=75, quantity=102, is_active=True, category=category_3)
        product_6 = Products(name='Пломбир класический', title='ТМ Молочный берег 100 гр',
                             price=80, quantity=12, is_active=True, category=category_3)
        session = self.__session()
        session.add_all([category_1, category_2, category_3])
        session.add_all(
            [product_1, product_2, product_3, product_4, product_5, product_6])

        session.commit()
        session.close()

    def _set_client(self, session):
        email_config = config.get_email_config()
        client = Client(address='Москва', chat_id=0, email=email_config['SENDER_EMAIL'],
                        latitude=55.899121, longitude=37.426408, phone='',
                        title='ИП Иванов А.И.', user_name='ivan_ai')
        session.add(client)

    def _set_store(self, session):
        store = Store(address='Москва, Химки', latitude=55.906430, longitude=37.459161,
                      price_km=50.0, title='Склад №1')
        session.add(store)

    def check_clients(self):
        clients = self.get_clients()
        if not clients:
            session = self.__session()
            self._set_client(session)
            self._set_store(session)
            session.commit()
            session.close()

    def select_single_product(self, rownum):
        """
        Возвращает одну строку товара с номером rownum
        """
        session=self.__session()
        result = session.query(Products).filter_by(id=rownum).first()
        session.close()
        return result

    def select_single_product_name(self, rownum):
        """
        Возвращает название товара в соответствии с номером rownum
        """
        session = self.__session()
        result = session.query(Products.name).filter_by(id=rownum).first()
        session.close()
        return result.name

    def select_single_product_quantity(self, rownum):
        """
        Возвращает количество товара в соответствии с номером rownum
        """
        session = self.__session()
        result = session.query(
            Products.quantity).filter_by(id=rownum).one()
        session.close()
        return result.quantity

    def select_single_product_title(self, rownum):
        """
        Возвращает title товара в соответствии с номером rownum
        """
        session = self.__session()
        result = session.query(Products.title).filter_by(id=rownum).one()
        session.close()
        return result.title

    def select_single_product_price(self, rownum):
        """
        Возвращает price товара в соответствии с номером rownum
        """
        session = self.__session()
        result = session.query(Products.price).filter_by(id=rownum).one()
        session.close()
        return result.price

    def select_all_products(self):
        """
        Возвращает все строки товаров
        """
        session = self.__session()
        result = session.query(Products).all()
        session.close()
        return result

    def select_all_products_category(self, category):
        """
        Возвращает все строки товара категории
        """
        session = self.__session()
        result = session.query(Products).filter_by(
            category_id=category).all()
        session.close()
        return result

    def select_all_id_category(self):
        """
        Возвращает все строки товара категории
        """
        session = self.__session()
        result = session.query(Category.id).all()
        session.close()
        return result

    def select_count_products_category(self, category):
        """
        Возвращает количество всех строк товара категории
        """
        session = self.__session()
        result = session.query(Products).filter_by(
            category_id=category).count()
        session.close()
        return result

    def count_rows_products(self):
        """
        Возвращает количество строк товара
        """
        session = self.__session()
        result = session.query(Products).count()
        session.close()
        return result

    def update_product_value(self, rownum, name, value):
        """
        Обновляет данные указанной строки товара
        """
        session = self.__session()
        session.query(Products).filter_by(
            id=rownum).update({name: value})
        session.commit()
        session.close()

    def delete_product(self, rownum):
        """
        Удаляет данные указанной строки товара
        """
        session = self.__session()
        session.query(Products).filter_by(id=rownum).delete()
        session.commit()
        session.close()

    # Работа с заказом
    def  _add_orders(self, quantity, product_id, user_id,):
        """
        Метод заполнения заказа
        """
        session = self.__session()
        # получаем список всех product_id
        all_id_product = self.select_all_product_id()
        # если данные есть в списке, обновляем таблицы заказа и продуктов
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)

            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        # если данных нет, создаем новый объект заказа
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)

        session.add(order)
        session.commit()
        session.close()

    def decrease_product(self, product_id, quantity):
        """
        check if quantity enough and decrease quantity of product
        :param product_id:
        :param quantity:
        :return True: if quantity enough, False: otherwise
        """
        session = self.__session()
        product = session.query(Products).filter_by(id=product_id).first()
        if product.quantity >= quantity:
            product.quantity -= quantity
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False

    def increase_product(self, product_id, quantity):
        """
        increase quantity of product - return to store from order
        :param product_id:
        :param quantity:
        :return:
        """
        session = self.__session()
        product = session.query(Products).filter_by(id=product_id).first()
        try:
            product.quantity += quantity
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.close()
            return False

    def select_all_product_id(self):
        """
        Возвращает все id товара в заказе
        """
        session = self.__session()
        result = session.query(Order.product_id).all()
        session.close()
        # конвертируем результат выборки в вид [1,3,5...]
        return utility._convert(result)

    def get_order(self, order_id):
        session = self.__session()
        order = session.query(Order).filter_by(id=order_id).first()
        session.close()
        return order

    def get_order_items(self, order_id):
        """
        load order items from orders by order_id
        """
        session = self.__session()
        result = session.query(Order).filter_by(order_id=order_id).order_by(Order.id).all()
        session.close()
        return result

    def update_order_value(self, product_id, name, value):
        """
        Обновляет данные указанной строки заказа
        """
        session = self.__session()
        self._session.query(Order).filter_by(
            product_id=product_id).update({name: value})
        session.commit()
        session.close()

    def delete_all_order(self):
        """
        Удаляет данные всего заказа
        """
        session = self.__session()
        all_id_orders = self.select_all_order_id()

        for itm in all_id_orders:
            session.query(Order).filter_by(id=itm).delete()
            session.commit()
        session.close()

    def delete_order(self, product_id):
        """
        Удаляет данные указанной строки заказа
        """
        session = self.__session()
        session.query(Order).filter_by(product_id=product_id).delete()
        session.commit()
        session.close()

    def select_order_quantity(self, product_id):
        """
        Возвращает количество товара в соответствии с номером rownum
        """
        session = self.__session()
        result = session.query(Order.quantity).filter_by(
            product_id=product_id).one()
        session.close()
        return result.quantity

    def count_rows_order(self):
        """
        Возвращает количество строк заказа
        """
        session = self.__session()
        result = session.query(Order).count()
        session.close()
        return result

    def select_all_order_id(self):
        """
        Возвращает все id заказа
        """
        session = self.__session()
        result = session.query(Order.id).all()
        session.close()
        return utility._convert(result)

    def select_single_order_id(self, rownum):
        """
        Возвращает id заказа с номером rownum
        """
        session = self.__session()
        result = session.query(Order.id).filter_by(id=rownum).one()
        session.close()
        return result

    # Working with order info
    def get_orders_info(self, trader_id):
        """
        load order info from db by trader_id
        """
        session = self.__session()
        result = session.query(OrderInfo).filter_by(trader_id=trader_id).all()
        session.close()
        return result

    def get_order_info(self, order_id):
        session = self.__session()
        order_info = session.query(OrderInfo).filter_by(id=order_id).first()
        session.close()
        return order_info

    def get_order_status(self, trader_id, status=config.Status.New):
        session = self.__session()
        order_info = session.query(OrderInfo).filter_by(trader_id=trader_id, status=status).first()
        session.close()
        return order_info

    def get_orders_status(self, status=config.Status.New):
        session = self.__session()
        order_info = session.query(OrderInfo).filter_by(status=status).all()
        session.close()
        return order_info

    def get_order_current(self, trader_id):
        session = self.__session()
        order_info = session.query(OrderInfo).filter_by(trader_id=trader_id, is_current=True).first()
        session.close()
        return order_info

    def set_order_current(self, trader_id, order_id):
        """
        set selected trader's order to current
        :param trader_id:
        :param order_id:
        :return:
        """
        session = self.__session()
        session.query(OrderInfo).filter_by(trader_id=trader_id).update({OrderInfo.is_current: False})
        # self.update_element()
        session.commit()
        order_info = session.query(OrderInfo).filter_by(id=order_id).first()
        order_info.is_current = True
        # self.update_element()
        session.commit()
        session.close()

    # Working with user
    def get_user(self, chat_id):
        session = self.__session()
        try:
            user = session.query(User).filter_by(chat_id=chat_id).first()
            session.close()
            return user
        except Exception as e:
            print(e)
            session.close()
            return None

    def get_user_id(self, user_id):
        session = self.__session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user

    # Working with clients
    def get_clients(self):
        """
        get list of clients
        :return result: all clients query list
        """
        session = self.__session()
        try:
            result = session.query(Client).all()
            session.close()
            return result
        except Exception as e:
            print(e)
            session.close()

    def get_client(self, client_id):
        session = self.__session()
        result = session.query(Client).filter_by(id=client_id).first()
        session.close()
        return result

    # Working with store
    def get_stores(self):
        """
        get list of stores
        :return result: all stores query list
        """
        session = self.__session()
        result = session.query(Store).all()
        session.close()
        return result

    # Working with session
    def close(self):
        """ Закрывает сесию """
        self._session.close()

    def save_element(self, element):
        """
        save element in database, return id of element
        """
        session = self.__session()
        session.add(element)
        session.commit()
        element_id = element.id
        session.close()
        return element_id

    def delete_element(self, element):
        """
        delete an element from Database
        :param element:
        :return:
        """
        session = self.__session()
        session.delete(element)
        session.commit()

    def save_elements(self, elements):
        session = self.__session()
        session.add_all(elements)
        session.commit()
        session.close()
