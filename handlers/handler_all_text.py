import json
from os import path
# импортируем настройки и утилиты
from settings import config
# импортируем ответ пользователю
from settings.message import MESSAGES
# импортируем класс родитель
from handlers.handler import Handler
from models.default_user import DefaultUser
from models.user import User
from models.order_trading import TraderUser
from reports.reports import ReportInvoice


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопоки
    """
    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопоку Выбрать товар.
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_info(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопоку TradingStore.
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопоку settings.
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_product(self, message, product):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопоки каталога товаров.
        """
        trader_user = self._get_current_trader(message)
        self.bot.send_message(message.chat.id, 'Категория ' + config.KEYBOARD[product],
                              reply_markup=\
                              self.keybords.set_select_category(trader=trader_user,
                                                                category=config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_back(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку back.
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    # -------------------------- working with order form --------------------------------------
    def pressed_btn_order(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку order - start work with it
        """
        trader_user = self._get_current_trader(message)
        trader_user.load_current(db=self.BD)
        if trader_user.order_items.number_positions > 0:
            # current order has a order positions
            # get current order item, set current first if there is no current order
            order_item = trader_user.order_items.current_get(db=self.BD)
            # send the message - fill the form
            self.send_message_order(message, order_item, trader_user)
        else:
            # current order has not a positions
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку back_step.
        """
        trader_user = self._get_current_trader(message)
        trader_user.load_current(db=self.BD)
        if trader_user.order_items.number_positions > 0:
            # current order has a order positions
            # get previous order item
            order_item = trader_user.order_items.current_prev(db=self.BD)
            # send the message - fill the form
            if not order_item is None:
                self.send_message_order(message, order_item, trader_user)
        else:
            # current order has not a positions
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_next_step(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку next_step.
        """
        trader_user = self._get_current_trader(message)
        trader_user.load_current(db=self.BD)
        if trader_user.order_items.number_positions > 0:
            # current order has a order positions
            # get next order item
            order_item = trader_user.order_items.current_next(db=self.BD)
            # send the message - fill the form
            if not order_item is None:
                self.send_message_order(message, order_item, trader_user)
        else:
            # current order has not a positions
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_down(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку douwn.
        """
        # получаем список всех товаров в заказе
        trader_user = self._get_current_trader(message)
        trader_user.load_current(db=self.BD)
        # получаем количество конкретной позиции в заказе
        order_item = trader_user.order_items.current_get(db=self.BD)
        trader_user.dec_item(db=self.BD, product_id=order_item.product_id)
        # отправляем ответ пользователю
        self.send_message_order(message, order_item, trader_user)

    def pressed_btn_up(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку up.
        """
        # получаем список всех товаров в заказе
        trader_user = self._get_current_trader(message)
        trader_user.load_current(db=self.BD)
        # получаем количество конкретной позиции в заказе
        order_item = trader_user.order_items.current_get(db=self.BD)
        trader_user.add_item(db=self.BD, product_id=order_item.product_id)
        # отправляем ответ пользователю
        self.send_message_order(message, order_item, trader_user)

    def pressed_btn_x(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку x удалить позицию шага.
        """
        # получаем список всех product_id заказа
        # count = self.BD.select_all_product_id()
        trader_user = self._get_current_trader(message)
        trader_user.load_current(db=self.BD)
        # если список не пуст
        order_item = trader_user.order_items.current_get(db=self.BD)
        trader_user.del_item(db=self.BD, product_id=order_item.product_id)
        # если список не пуст
        if trader_user.order_items.number_positions > 0:
            # отправляем пользователю сообщение
            order_item = trader_user.order_items.current_get(db=self.BD)
            # send the message - fill the form
            self.send_message_order(message, order_item, trader_user)
        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_apply(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку apply.
        """
        trader_user = self._get_current_trader(message)
        trader_user.load_current(db=self.BD)
        # if has order items
        if trader_user.order_items.number_positions > 0:
            # отправляем ответ пользователю
            if not trader_user.order.has_client():
                self.bot.send_message(message.chat.id,
                                      'Укажите адресата доставки заказа:',
                                      reply_markup=self.keybords.set_select_client(trader=trader_user))
                message_text = 'Выбор адресата'
            else:
                trader_user.order.delivery_cost(db=self.BD)
                self._perform_order(trader_user)
                message_text = MESSAGES['apply'].format(trader_user.order_items.total_price(self.BD),
                                                        trader_user.order_items.number_items)
        else:
            # если товара нет в заказе отправляем сообщение
            message_text = MESSAGES['no_orders']
        self.bot.send_message(message.chat.id, message_text, parse_mode="HTML")
        # # отчищаем данные с заказа
        # self.BD.delete_all_order()

    def send_message_order(self, message, order_item, trader_user):
        """
        отправляет ответ пользователю при выполнении различных действий - fill the order form
        """
        product = self.BD.select_single_product(order_item.product_id)
        step = {'number': order_item.number,
                'quantity': order_item.quantity,
                'positions': trader_user.order_items.number_positions,
                'total_price': trader_user.order_items.total_price(self.BD)}
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(order_item.number),
                              parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].format(product.name,
                                                       product.title,
                                                       product.price,
                                                       order_item.quantity),
                              parse_mode="HTML",                                          
                              reply_markup=self.keybords.orders_menu(step=json.dumps(step)))

    def _perform_order(self, trader: TraderUser):
        """
        perform order - clear current items, set next status Work
        :param trader:
        :return:
        """
        trader.order.status(status=config.Status.Work)
        trader.order.save(self.BD)
        trader.order_items.current_clear(self.BD)
    # -------------------------- end of working with order form ------------------------------------

    def _get_trader_orders(self, message):
        """
        get list of orders of current trader
        :param message:
        :return: None
        """
        trader_user = self._get_current_trader(message)
        orders = trader_user.get_orders(self.BD)
        if orders:
            msg = 'Пожалуйста, выберите заказ для работы:'
            self.bot.send_message(message.chat.id, msg,
                                  reply_markup=self.keybords.orders_info_menu(trader_user))
        else:
            msg = 'У Вас нет заказов для работы'
            self.bot.send_message(message.chat.id, msg, reply_markup=self.keybords.start_menu())

    def _add_trader(self, message):
        """
        add new user with role 'Trader'
        """
        user = User(chat_id=message.chat.id, role=config.Role.Trader)
        trader_id = self.BD.save_element(user)
        trader_user = TraderUser(trader_id=trader_id, user_name=message.from_user.first_name)
        trader_user.save(self.BD)
        self.bot.send_message(message.chat.id, 'Приятной работы',
                              reply_markup=self.keybords.start_menu())

    def _get_current_trader(self, message):
        """
        get current trader
        :param message:
        :return: TraderUser
        """
        user = self.BD.get_user(chat_id=message.chat.id)
        return TraderUser(user.id, message.from_user.first_name)

    def _add_admin(self, message):
        """
        add new user with role 'Admin'
        :param message:
        :return:
        """
        user = User(chat_id=message.chat.id, role=config.Role.Admin)
        self.BD.save_element(user)
        self.bot.send_message(message.chat.id, 'Приятной работы',
                              reply_markup=self.keybords.admin_menu())

    def _add_keeper(self, message):
        """
        add new user with role 'Keeper'
        :param message:
        :return:
        """
        user = User(chat_id=message.chat.id, role=config.Role.Keeper)
        self.BD.save_element(user)
        self.bot.send_message(message.chat.id, 'Приятной работы',
                              reply_markup=self.keybords.keeper_menu())

    def handle(self):
        """обработчик(декоратор) сообщений,
        который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        """
        @self.bot.message_handler(func=lambda message: message.text in config.KEYBOARD.values())
        def handle(message):
            # ********** меню (выбор роли)                          **********
            new_user = DefaultUser(chat_id=message.chat.id)
            reply = 'Введите пароль'
            if message.text == config.KEYBOARD['TRADER']:
                new_user.dialog_status = config.DialogState.UserTrader
                # self._add_trader(message)
            if message.text == config.KEYBOARD['KEEPER']:
                new_user.dialog_status = config.DialogState.UserKeeper
            if message.text == config.KEYBOARD['ADMIN']:
                new_user.dialog_status = config.DialogState.UserAdmin
                # self._add_admin(message)
            self.bot.send_message(message.chat.id, reply)

            # ********** меню (выбор категории, настройки, сведения)**********
            if message.text == config.KEYBOARD['CHOOSE_ORDER']:
                self._get_trader_orders(message)
            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            # ********** меню (категории товара, ПФ, Бакалея, Мороженое)**********
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            if message.text == config.KEYBOARD['ORDER']:
                self.pressed_btn_order(message)
                # если есть заказ
                # if self.BD.count_rows_order() > 0:
                #     self.pressed_btn_order(message)
                # else:
                #     self.bot.send_message(message.chat.id,MESSAGES['no_orders'],
                #                           parse_mode="HTML",
                #                           reply_markup=self.keybords.category_menu())

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            # ********** меню (Заказа)**********

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_btn_apply(message)
            # иные нажатия и ввод данных пользователем
            # else:
            #     self.bot.send_message(message.chat.id, message.text)

        # ********** input password **********
        @self.bot.message_handler(func=lambda message: _dialog_password(message.chat.id))
        def _check_password(message):
            """
            check password depends on user's role
            :param message:
            :return:
            """
            new_user = DefaultUser(chat_id=message.chat.id)
            if new_user.check_password(message.text):
                if new_user.dialog_status == config.DialogState.UserTrader:
                    self._add_trader(message)
                if new_user.dialog_status == config.DialogState.UserKeeper:
                    self._add_keeper(message)
                if new_user.dialog_status == config.DialogState.UserAdmin:
                    self._add_admin(message)
                new_user.dialog_status = config.DialogState.NoDialog
            else:
                self.bot.send_message(message.chat.id, 'Повторите ввод')

        def _dialog_password(chat_id):
            """
            get status dialog from default user
            :param chat_id:
            :return dialog_status:
            """
            new_user = DefaultUser(chat_id=chat_id)
            return new_user.dialog_status == config.DialogState.UserTrader\
                or new_user.dialog_status == config.DialogState.UserKeeper\
                or new_user.dialog_status == config.DialogState.UserAdmin
