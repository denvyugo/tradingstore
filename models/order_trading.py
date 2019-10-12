"""
Model for working trader user with orders
"""
from datetime import datetime
from collections import OrderedDict
from geopy.distance import distance
from DB.DBAlchemy import DBManager
from models.order import Order
from models.order_info import OrderInfo
from models.trader import Trader
from settings.config import Status


"""class for order item"""
class OrderItem:
    def __init__(self, order_spec, number, product_id, quantity=1, is_current=False, item_id=0):
        self._id = item_id
        self._order_spec = order_spec
        self.number = number
        self.is_current = is_current
        self._product_id = product_id
        self._quantity = quantity

    @property
    def product_id(self):
        return self._product_id

    @property
    def quantity(self):
        return self._quantity

    def save(self, db: DBManager):
        if self._id:
            order = db.get_order(self._id)
            order.is_current = self.is_current
            order.product_id = self.product_id
            order.quantity = self.quantity
            db.save_element(order)
        else:
            db.save_element(self.get_order())

    def delete(self, db: DBManager):
        if self._id:
            order = db.get_order(self._id)
            db.delete_element(order)

    def get_order(self):
        order = Order(order_id=self._order_spec.id,
                      is_current=self.is_current,
                      product_id=self.product_id,
                      quantity = self.quantity)
        return order

    def __repr__(self):
        """
        Метод возвращает формальное строковое представление указанного объекта
        """
        return "Order: {}, product id = {}, qty = {}".format(self._id, self.product_id, self.quantity)


"""class for items of order, implements Iterator"""
class OrderItems:
    def __init__(self):
        self._orders = OrderedDict()

    def __iter__(self):
        return iter(self._orders.values())

    def _add(self, order_spec, product_id, quantity=1):
        if product_id not in self._orders:
            number = len(self._orders) + 1
            order_item = OrderItem(order_spec=order_spec, number=number, product_id=product_id, quantity=quantity)
            self._orders[product_id] = order_item
        else:
            order_item = self._orders[product_id]
            order_item._quantity += quantity

    def _dec(self, product_id, quantity=1):
        """
        check possibility of decrease number of item
        :param product_id:
        :param quantity:
        :return True: if possible to decrease, False: otherwise
        """
        if product_id in self._orders:
            order_item = self._orders[product_id]
            if order_item.quantity > quantity:
                order_item._quantity -= quantity
                return True
            else:
                return False

    def _del(self, db: DBManager, order_spec, product_id):
        """
        delete order item position
        :param db:
        :param product_id:
        :return:
        """
        if product_id in self._orders:
            order_item = self._orders[product_id]
            numbers = self.number_positions
            if db.increase_product(product_id=product_id, quantity=order_item.quantity):
                if numbers > 1:
                    if 1 < order_item.number < numbers or order_item.number == numbers:
                        self.current_prev(db)
                    elif order_item.number == 1:
                        self.current_next(db)
                order_item.delete(db)
                self._orders = OrderedDict()
                self._load(db=db, order_spec=order_spec)

    @property
    def number_positions(self):
        return len(self._orders)

    @property
    def number_items(self):
        sum_quantity = 0
        for order_item in self._orders.values():
            sum_quantity += order_item.quantity
        return sum_quantity

    def total_price(self, db: DBManager):
        price = 0
        for order_item in self._orders.values():
            product = db.select_single_product(rownum=order_item.product_id)
            price += product.price * order_item.quantity
        return round(price, 2)

    def current_get(self, db: DBManager):
        """
        get current or set current & get first item of order
        :param db:
        :return:
        """
        for order in self._orders.values():
            if order.is_current:
                break
        else:
            product_id = list(self._orders.keys())[0]
            order = self._orders[product_id]
            order.is_current = True
            order.save(db)
        return order

    def current_next(self, db: DBManager):
        """
        make the next current order if present
        :param db:
        :return order: if it possible get next position, current position: otherwise
        """
        product_id = list(reversed(self._orders.keys()))[0]
        order = self._orders[product_id]
        if not order.is_current:
            next_current = False
            for order in self._orders.values():
                if next_current:
                    order.is_current = next_current
                    order.save(db)
                    break
                if order.is_current:
                    order.is_current = False
                    order.save(db)
                    next_current = True
            if next_current:
                return order
        else:
            return self._orders[product_id]

    def current_prev(self, db: DBManager):
        """
        make the previous current order if present
        :param db:
        :return order: if it possible get previous position, current position: otherwise
        """
        product_id = list(self._orders.keys())[0]
        order = self._orders[product_id]
        if not order.is_current:
            prev_current = False
            for order in reversed(self._orders.values()):
                if prev_current:
                    order.is_current = prev_current
                    order.save(db)
                    break
                if order.is_current:
                    order.is_current = False
                    order.save(db)
                    prev_current = True
            if prev_current:
                return order
        else:
            return self._orders[product_id]

    def current_clear(self, db: DBManager):
        """
        clear is_current status for each order item
        :param db:
        :return:
        """
        for order in self._orders.values():
            order.is_current = False
            order.save(db)

    def _load(self, db: DBManager, order_spec):
        products = db.get_order_items(order_spec.id)
        number = 0
        for order in products:
            number += 1
            order_item = OrderItem(order_spec=order_spec,
                                   number=number,
                                   is_current=order.is_current,
                                   product_id=order.product_id,
                                   quantity=order.quantity,
                                   item_id=order.id)
            order_item.order_id = order.order_id
            self._orders[order_item.product_id] = order_item

    def delete_all(self):
        pass

    def _save(self, db: DBManager):
        for order in self._orders.values():
            order.save(db)


"""class for order info"""
class OrderSpec:
    def __init__(self, trader_id):
        self._client = 0
        self._date = None
        self._delivery_cost = 0
        self._current = True
        self._status = Status.New
        self._store = 0
        self._trader = trader_id
        self._id = 0

    @property
    def date(self):
        return self._date

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, order_id):
        self._id = order_id

    def has_client(self):
        return self._client > 0

    def get_client(self):
        return self._client

    def set_client(self, client_id):
        self._client = client_id

    def delivery_cost(self, db: DBManager):
        """
        calculate cost of delivery from nearest store
        :param db: get addresses of stores
        :return delivery_cost: cost is distance multiply to price_km of nearest store to client
        """
        print('DELIVERY COST:', self._delivery_cost)
        if self._delivery_cost is None or self._delivery_cost == 0:
            if self._client == 0:
                return 0
            if self._store == 0:
                # get nearest store
                client_distance, store_id, price_km = self._get_store_near(db)
                self._store = store_id
                self._delivery_cost = round(client_distance * price_km, 2)
        return self._delivery_cost

    def status(self, status):
        if status != 0:
            print('STATUS:', status)
            self._current = False
        self._status = status

    def load(self, db: DBManager, order_id):
        self._id = order_id
        order_info = db.get_order_info(order_id)
        self._client = order_info.client_id
        self._current = order_info.is_current
        self._date = order_info.order_date
        self._delivery_cost = order_info.delivery_cost
        self._status = order_info.status
        self._store = order_info.store_id

    def save(self, db: DBManager):
        if self._id:
            order = db.get_order_info(self._id)
            order.is_current = self._current
            order.client_id = self._client
            order.delivery_cost = self._delivery_cost
            order.order_date = self._date
            order.status = self._status
            order.store_id = self._store
            db.save_element(order)
        else:
            self._date = datetime.now()
            order = self._get_order_info()
            self._id = db.save_element(order)
        return order

    def _get_order_info(self):
        order_info = OrderInfo(client_id=self._client,
                               is_current=self._current,
                               delivery_cost=self._delivery_cost,
                               order_date=self._date,
                               status=self._status,
                               store_id=self._store,
                               trader_id=self._trader)
        return order_info

    def _get_store_near(self, db: DBManager):
        client = db.get_client(self._client)
        stores = db.get_stores()
        client_distance = 0.0
        store_distance = 0.0
        store_id = 0
        price_km = 0.0
        client_location = (client.latitude, client.longitude)
        for store in stores:
            store_location = (store.latitude, store.longitude)
            if client_distance == 0.0:
                client_distance = distance(client_location, store_location).kilometers
                store_id = store.id
                price_km = store.price_km
                continue
            store_distance = distance(client_location, store_location).kilometers
            if store_distance < client_distance:
                client_distance = store_distance
                store_id = store.id
                price_km = store.price_km
        return client_distance, store_id, price_km


"""class for Trader"""
class TraderUser:
    def __init__(self, trader_id, user_name=''):
        self._id = trader_id
        self.order_items = OrderItems()
        self.order = OrderSpec(self._id)
        self._name = user_name
        self._chat_id = 0

    @property
    def id(self):
        return self._id

    @property
    def chat_id(self):
        return self._chat_id

    def add_item(self, db: DBManager, product_id, quantity=1):
        """
        add item to order, if enough product quantity
        :param db: link to DBManager
        :param product_id:
        :param quantity:
        :return True: if enough products, False: otherwise
        """
        if self.order.id == 0:
            self.order.save(db)
        # check if product quantity enough
        if db.decrease_product(product_id=product_id, quantity=quantity):
            self.order_items._add(order_spec=self.order,
                              product_id=product_id,
                              quantity=quantity)
            self.order_items._save(db)
            return True
        else:
            return False

    def dec_item(self, db: DBManager, product_id, quantity=1):
        """
        decrease number of order item
        :param db: link to DBManager
        :param product_id:
        :param quantity:
        :return:
        """
        if self.order.id > 0:
            # return quantity of product to store
            if self.order_items._dec(product_id=product_id, quantity=quantity):
                if db.increase_product(product_id=product_id, quantity=quantity):
                    self.order_items._save(db)

    def del_item(self, db: DBManager, product_id):
        """
        delete order item from order
        :param db:
        :param product_id:
        :return:
        """
        if self.order.id > 0:
            self.order_items._del(db=db, order_spec=self.order, product_id=product_id)

    def get_orders(self, db: DBManager):
        """
        get list of orders from order_info table or get only one current order
        """
        order = self._load_current_order(db=db)
        if order:
            return [order]
        else:
            orders = db.get_orders_info(self._id)
            return orders

    def load_order(self, db: DBManager, order_id):
        """
        load order info by order_id
        """
        self._load(db=db)
        self.order.load(db=db, order_id=order_id)
        self.order_items._load(db=db, order_spec=self.order)

    def load_current(self, db: DBManager):
        """
        load current order if exist
        :param db:
        :return:
        """
        order = self._load_current_order(db=db)
        if order:
            self.load_order(db=db, order_id=order.id)

    def save_order(self, db: DBManager):
        """save order items in DB if order info (OrderSpec) is presented"""
        self.order.save(db)
        if self.order.id:
            self.order_items._save(db)

    def save(self, db):
        print('trader id: ', self._id)
        trader = Trader(user_id=self._id, phone='', user_name=self._name)
        db.save_element(trader)

    def _load(self, db: DBManager):
        user = db.get_user_id(self._id)
        if user:
            self._chat_id = user.chat_id

    def _load_current_order(self, db: DBManager):
        return db.get_order_current(trader_id=self._id)
