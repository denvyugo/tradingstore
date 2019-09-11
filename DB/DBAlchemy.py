import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import config
from settings import utility

from DB.dbcore import Base

from models.category import Category
from models.product import Products
from models.order import Order


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
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not os.path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

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

        self._session.add_all([category_1, category_2, category_3])
        self._session.add_all(
            [product_1, product_2, product_3, product_4, product_5, product_6])

        self._session.commit()
        self.close()

    def select_single_product(self, rownum):
        """ 
        Возвращает одну строку товара с номером rownum 
        """
        result = self._session.query(Products).filter_by(id=rownum).all()
        self.close()
        return result

    def select_single_product_name(self, rownum):
        """ 
        Возвращает название товара в соответствии с номером rownum 
        """
        result = self._session.query(Products.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_quantity(self, rownum):
        """ 
        Возвращает количество товара в соответствии с номером rownum 
        """
        result = self._session.query(
            Products.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def select_single_product_title(self, rownum):
        """ 
        Возвращает title товара в соответствии с номером rownum 
        """
        result = self._session.query(Products.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        """ 
        Возвращает price товара в соответствии с номером rownum 
        """
        result = self._session.query(Products.price).filter_by(id=rownum).one()
        self.close()
        return result.price

    def select_all_products(self):
        """ 
        Возвращает все строки товаров
        """
        result = self._session.query(Products).all()
        self.close()
        return result

    def select_all_products_category(self, category):
        """ 
        Возвращает все строки товара категории 
        """
        result = self._session.query(Products).filter_by(
            category_id=category).all()
        self.close()
        return result

    def select_all_id_category(self):
        """ 
        Возвращает все строки товара категории 
        """
        result = self._session.query(Category.id).all()
        self.close()
        return result

    def select_count_products_category(self, category):
        """ 
        Возвращает количество всех строк товара категории 
        """
        result = self._session.query(Products).filter_by(
            category_id=category).count()
        self.close()
        return result

    def count_rows_products(self):
        """ 
        Возвращает количество строк товара
        """
        result = self._session.query(Products).count()
        self.close()
        return result

    def update_product_value(self, rownum, name, value):
        """ 
        Обновляет данные указанной строки товара 
        """
        self._session.query(Products).filter_by(
            id=rownum).update({name: value})
        self._session.commit()
        self.close()

    def delete_product(self, rownum):
        """ 
        Удаляет данные указанной строки товара 
        """
        self._session.query(Products).filter_by(id=rownum).delete()
        self._session.commit()
        self.close()

    # Работа с заказом
    def _add_orders(self, quantity, product_id, user_id,):
        """
        Метод заполнения заказа
        """
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

        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id(self):
        """ 
        Возвращает все id товара в заказе
        """
        result = self._session.query(Order.product_id).all()
        self.close()
        # конвертируем результат выборки в вид [1,3,5...]
        return utility._convert(result)

    def update_order_value(self, product_id, name, value):
        """ 
        Обновляет данные указанной строки заказа 
        """
        self._session.query(Order).filter_by(
            product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def delete_all_order(self):
        """ 
        Удаляет данные всего заказа 
        """
        all_id_orders = self.select_all_order_id()

        for itm in all_id_orders:
            self._session.query(Order).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def delete_order(self, product_id):
        """ 
        Удаляет данные указанной строки заказа 
        """
        self._session.query(Order).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def select_order_quantity(self, product_id):
        """ 
        Возвращает количество товара в соответствии с номером rownum 
        """
        result = self._session.query(Order.quantity).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity

    def count_rows_order(self):
        """  
        Возвращает количество строк заказа
        """
        result = self._session.query(Order).count()
        self.close()
        return result

    def select_all_order_id(self):
        """ 
        Возвращает все id заказа
        """
        result = self._session.query(Order.id).all()
        self.close()
        return utility._convert(result)

    def select_single_order_id(self, rownum):
        """ 
        Возвращает id заказа с номером rownum 
        """
        result = self._session.query(Order.id).filter_by(id=rownum).one()

        return result

    def close(self):
        """ Закрывает сесию """
        self._session.close()
