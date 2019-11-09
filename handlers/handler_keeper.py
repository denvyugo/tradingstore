# импортируем настройки и утилиты
from settings.config import KEEPER, Status
# импортируем класс родитель
from handlers.handler import Handler
from models.keeper import Keeper


class HandlerKeeper(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def handle(self):
        @self.bot.message_handler(func=lambda message: message.text == KEEPER['GET_ORDERS'])
        def orders_list(message):
            """
            get order list from db with status 'Work'
            :param message:
            :return:
            """
            keeper_user = Keeper(chat_id=message.chat.id)
            keeper_user.order_status = Status.Work
            orders = keeper_user.get_orders(db=self.BD)
            if orders:
                reply = 'Выберите собранный заказ'
                markup = self.keybords.keeper_orders_menu(keeper_id=keeper_user.chat_id,
                                                          orders=orders,
                                                          next_status=Status.Complete)
            else:
                reply = 'У Вас нет заказов в работе'
                markup = None
            self.bot.send_message(keeper_user.chat_id, reply, reply_markup=markup)
