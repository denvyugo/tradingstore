import json
# импортируем класс родитель
from handlers.handler import Handler
# импортируем сообщения пользователю
from settings.message import MESSAGES
from models.order_trading import TraderUser
from models.keeper import Keeper


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на инлайн кнопоки
    """

    def __init__(self, bot):
        super().__init__(bot)

    def _get_trader(self, trader_id):
        """
        enter in current order and display form for work with it
        :param trader_id:
        :return TraderUser:
        """
        trader_user = TraderUser(trader_id=trader_id)
        trader_user.load_current(db=self.BD)
        return trader_user

    def pressed_btn_product(self, call, code):
        """
        обрабатывает входящие запросы на нажатие кнопок товара inline
        """
        trader = TraderUser(code['t'])
        if code['o'] is None:
            trader.order.save(self.BD)
        else:
            trader.load_order(db=self.BD, order_id=code['o'])
        if trader.add_item(db=self.BD, product_id=code['p']):
            product = self.BD.select_single_product(code['p'])
            self.bot.answer_callback_query(call.id,
                                       MESSAGES['product_order'].format(product.name,
                                                                        product.title,
                                                                        product.price,
                                                                        product.quantity),
                                       show_alert=True)
        else:
            self.bot.answer_callback_query(call.id, 'Недостаточно товаров на складе', show_alert=True)
        
    def pressed_btn_order(self, code):
        """
        make selected order status current
        :param code:
        :return: None
        """
        self.BD.set_order_current(trader_id=code['t'], order_id=code['o'])
        trader = self._get_trader(trader_id=code['t'])
        msg = 'Выбран заказ №{}, можете продолжить работу с заказом или выбрать другой'.format(code['o'])
        self.bot.send_message(trader.chat_id, msg, reply_markup=self.keybords.current_order_menu())

    def pressed_btn_client(self, call, code):
        """
        add client to order
        :param call:
        :param code:
        :return:
        """
        trader = TraderUser(code['t'])
        trader.load_order(db=self.BD, order_id=code['o'])
        trader.order.set_client(client_id=code['c'])
        # calculate cost of delivery
        delivery_cost = trader.order.delivery_cost(db=self.BD)
        trader.order.save(db=self.BD)
        self.bot.answer_callback_query(call.id, 'Стоимость доставки {} рублей'.format(delivery_cost))

    def pressed_status_order(self, call, code):
        """
        change status of order by keeper user
        :param code:
        :return:
        """
        keeper = Keeper(code['k'])
        keeper.change_status(db=self.BD, order_id=code['o'], order_status=code['n'])
        self.bot.answer_callback_query(call.id,
                                       'Статус заказа изменён на: {} '.format(code['n']))

    def handle(self):
        #обработчик(декоратор) запросов от нажатия на кнопки товара.
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = json.loads(call.data)
            if code['m'] == 'p':
                self.pressed_btn_product(call, code)
            if code['m'] == 'o':
                self.pressed_btn_order(code=code)
            if code['m'] == 'c':
                self.pressed_btn_client(call=call, code=code)
            if code['m'] == 's':
                self.pressed_status_order(call=call, code=code)
