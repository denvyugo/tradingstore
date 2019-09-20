import json
# импортируем класс родитель
from handlers.handler import Handler
# импортируем сообщения пользователю
from settings.message import MESSAGES
from models.order_trading import TraderUser


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на инлайн кнопоки
    """

    def __init__(self, bot):
        super().__init__(bot)

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

    def handle(self):
        #обработчик(декоратор) запросов от нажатия на кнопки товара.
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = json.loads(call.data)
            if code['m'] == 'p':
                self.pressed_btn_product(call, code)
            if code['m'] == 'o':
                self.pressed_btn_order(code=code)
