"""
Model for working trader user with orders
"""
from datetime import datetime
from DB.DBAlchemy import DBManager
from models.order import Order
from models.order_info import OrderInfo
from models.trader import Trader


"""class for order item"""
class OrderItem:
    def __init__(self, order_spec, product_id, quantity=1, item_id=0):
        self._id = item_id
        self._order_spec = order_spec
        self.product_id = product_id
        self.quantity = quantity

    def save(self):
        db = DBManager()
        if self._id:
            order = db.get_order(self._id)
            order.product_id = self.product_id
            order.quantity = self.quantity
            db.update_element()
        else:
            db.save_element(self.get_order())

    def get_order(self):
        order = Order(order_id=self._order_spec.id,
                      product_id=self.product_id,
                      quantity = self.quantity)
        return order


"""class for items of order, implements Iterator"""
class OrderItems:
    def __init__(self):
        self._orders = {}

    def __iter__(self):
        return iter(self._orders.values())

    def _add(self, order_spec, product_id, quantity=1):
        if product_id not in self._orders:
            order_item = OrderItem(order_spec=order_spec ,product_id=product_id, quantity=quantity)
            self._orders[product_id] = order_item
        else:
            order_item = self._orders[product_id]
            order_item.quantity += quantity

    @property
    def number_positions(self):
        return len(self._orders)

    @property
    def number_items(self):
        sum_quantity = 0
        for order_item in self._orders.values():
            sum_quantity += order_item.quantity
        return sum_quantity

    def _load(self, order_spec):
        db = DBManager()
        products = db.get_order_items(order_spec.id)
        for order in products:
            order_item = OrderItem(order_spec=order_spec,
                                   product_id=order.product_id,
                                   quantity=order.quantity,
                                   item_id=order.id)
            order_item.order_id = order.order_id
            self._orders[order_item.product_id] = order_item

    def status(self):
        pass

    def delete_all(self):
        pass

    def _save(self):
        for order in self._orders.values():
            order.save()


"""class for order info"""
class OrderSpec:
    def __init__(self, trader_id):
        self._client = 0
        self._date = None
        self._status = 'New'
        self._trader = trader_id
        self._id = 0

    @property
    def id(self):
        return self._id

    def set_client(self, client_id):
        self._client = client_id

    def load(self, order_id):
        self._id = order_id
        db = DBManager()
        order_info = db.get_order_info(order_id)
        self._client = order_info.client_id
        self._date = order_info.order_date
        self._status = order_info.status

    def save(self):
        db = DBManager()
        if self._id:
            order = db.get_order_info(self._id)
            order.client_id = self._client
            order.order_date = self._date
            order.status = self._status
            db.update_element()
        else:
            self._date = datetime.now()
            order_info = self._get_order_info()
            self._id = db.save_element(order_info)

    def _get_order_info(self):
        order_info = OrderInfo(client_id=self._client,
                               order_date=self._date,
                               status=self._status,
                               trader_id=self._trader)
        return order_info


"""class for Trader"""
class TraderUser:
    def __init__(self, trader_id, user_name=''):
        self._id = trader_id
        self.order_items = OrderItems()
        self.order = OrderSpec(self._id)
        self._name = user_name

    def add_item(self, product_id, quantity=1):
        self.order_items._add(order_spec=self.order,
                              product_id=product_id,
                              quantity=quantity)

    def get_orders(self, db):
        """
        get list of orders from order_info table
        """
        # db = DBManager()
        orders = db.get_orders_info(self._id)
        return orders

    def load_order(self, order_id):
        """load order info by order_id"""
        self.order.load(order_id)
        self.order_items._load(self.order)

    def save_order(self):
        """save order items in DB if order info (OrderSpec) is presented"""
        self.order.save()
        if self.order.id:
            self.order_items._save()

    def save(self, db):
        # db = DBManager()
        print('trader id: ', self._id)
        trader = Trader(user_id=self._id, phone='', user_name=self._name)
        db.save_element(trader)
