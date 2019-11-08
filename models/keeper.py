"""
Models for keeper users
"""
from DB.DBAlchemy import DBManager
from models.order_info import OrderInfo
from settings import config


class Keeper:
    def __init__(self, chat_id):
        self._chat_id = chat_id
        self._order_status = config.Status.Work

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def order_status(self):
        return self._order_status

    @order_status.setter
    def order_status(self, order_status):
        if order_status in config.Status:
            self._order_status = order_status

    def get_orders(self, db: DBManager):
        """
        get a list of orders with status like self._order_status
        from order_info table
        :param db:
        :return orders: list of order objects
        """
        orders = db.get_orders_status(status=self._order_status)
        return orders

    @staticmethod
    def change_status(db: DBManager, order_id, order_status):
        """
        change status of order
        :param db:
        :param order_id:
        :param order_status:
        :return:
        """
        order: OrderInfo = db.get_order_info(order_id=order_id)
        order.status = order_status
        db.save_element(order)
