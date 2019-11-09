"""
Models for keeper users
"""
from os import path
from DB.DBAlchemy import DBManager
from mail.mail import BotMail
from models.order_info import OrderInfo
from reports.reports import ReportInvoice
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

    def perform_invoice(self, db: DBManager, order_id):
        """
        perform invoice PDF file in directory invoices
        :param db:
        :param order_id:
        :return:
        """
        if config.is_company_info():
            info = config.company_info()
            invoice = ReportInvoice()
            invoice.company_info(info)
            order = db.get_order_info(order_id=order_id)
            client = db.get_client(order.client_id)
            invoice.set_order(date=order.order_date, number=order_id,
                              payer=client.title, address=client.address,
                              delivery=order.delivery_cost)
            order_items = db.get_order_items(order_id)
            for item in order_items:
                product = db.select_single_product(item.product_id)
                invoice.add_item(name=product.name, code=product.title, unit='шт.',
                                 quantity=item.quantity, price=product.price)
            invoice.make()
            _send_invoice_mail(client, order_id)

def _send_invoice_mail(client, order_id):
    """
    send invoice pdf file to client by email
    :param client:
    :return:
    """
    file_name = ReportInvoice.invoice_file(order_id)
    if path.exists(file_name):
        mail_item = BotMail()
        subject = 'Счёт №{}'.format(order_id)
        body = 'Добрый день, {}!\nВо вложении счёт на оплату заказа №{}'\
            .format(client.user_name, order_id)
        receiver = client.email
        mail_item.send_mail(subject, body, receiver, file_name)
