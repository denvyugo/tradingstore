# импортируем настройки и утилиты
from settings import config, utility
# импортируем ответ пользователю
from settings.message import MESSAGES
# импортируем класс родитель
from handlers.handler import Handler
from models.user import User
from models.order_trading import TraderUser

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
        self.bot.send_message(message.chat.id,MESSAGES['trading_store'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопоку settings.
        """
        self.bot.send_message(message.chat.id,MESSAGES['settings'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.settings_menu())

    def pressed_btn_product(self, message, product):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопоки каталога товаров.
        """
        trader_user = self._get_current_trader(message)
        self.bot.send_message(message.chat.id, 'Категория ' + config.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_category(trader_id=trader_user.id,
                                                                             category=config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keybords.category_menu())
    
    def pressed_btn_back(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку back.
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())
    
    def pressed_btn_order(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку order.
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество в каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step],quantity,message)

    def pressed_btn_back_step(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку back_step.
        """
        # уменьшаем шаг пока шаг не будет равет "0"
        if self.step > 0:
            self.step -=1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step],quantity,message)
    
    def pressed_btn_next_step(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку next_step.
        """
        # увеличиваем шаг пока шаг не будет равет количеству строк полей заказа с расчетом цены деления начиная с "0"
        if self.step < self.BD.count_rows_order()-1:
            self.step +=1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем еоличество конкретного товара в соответствие с шагом выборки 
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step],quantity,message)

    def pressed_btn_douwn(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку douwn.
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции в пролуктов
        quantity_product =self.BD.select_single_product_quantity(count[self.step])
        # если товар в заказе есть
        if quantity_order > 0:
            quantity_order -=1
            quantity_product +=1
            # вносим изменения в БД orders
            self.BD.update_order_value(count[self.step],'quantity',quantity_order)  
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],'quantity',quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step],quantity_order,message)
    
    def pressed_btn_up(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку up.
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции в пролуктов
        quantity_product =self.BD.select_single_product_quantity(count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order +=1
            quantity_product -=1
            # вносим изменения в БД orders
            self.BD.update_order_value(count[self.step],'quantity',quantity_order) 
            # вносим изменения в БД product 
            self.BD.update_product_value(count[self.step],'quantity',quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step],quantity_order,message)

    def pressed_btn_x(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку x удалить позицию шага.
        """
        # получаем список всех product_id заказа
        count = self.BD.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:
            # получаем количество конкретной позиции в заказе
            quantity_order = self.BD.select_order_quantity(count[self.step])
            # получаем количество товара к конкретной позиции заказа для возврата в product
            quantity_product =self.BD.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            # вносим изменения в БД orders
            self.BD.delete_order(count[self.step])
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],'quantity',quantity_product)
            # уменьшаем шаг
            self.step -= 1

        count = self.BD.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:

            quantity_order = self.BD.select_order_quantity(count[self.step])
            # отправляем пользователю сообщение
            self.send_message_order(count[self.step],quantity_order,message)

        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id,MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())
    
    def pressed_btn_apllay(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку apllay.
        """
        # отправляем ответ пользователю
        self.bot.send_message(message.chat.id, MESSAGES['applay'].format(utility.get_total_coas(self.BD),
                                                                         utility.get_total_quantity(self.BD)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.category_menu())
        # отчищаем данные с заказа
        self.BD.delete_all_order()

    def send_message_order(self,product_id,quantity,message):
        """
        отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id,MESSAGES['order_number'].format(self.step+1),parse_mode="HTML") 
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].format(self.BD.select_single_product_name(product_id),
                                                                        self.BD.select_single_product_title(product_id),
                                                                        self.BD.select_single_product_price(product_id),
                                                                        self.BD.select_order_quantity(product_id)),
                              parse_mode="HTML",                                          
                              reply_markup=self.keybords.orders_menu(self.step,quantity))

    def _get_trader_orders(self, message):
        """
        get list of orders of current trader
        :param message:
        :return: None
        """
        trader_user = self._get_current_trader(message)
        orders = trader_user.get_orders(self.BD)
        if len(orders):
            msg = 'Пожалуйста, выберите заказ для работы:'
            self.bot.send_message(message.chat.id, msg, reply_markup=self.keybords.orders_info_menu(trader_user))
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
        self.bot.send_message(message.chat.id, 'Приятной работы', reply_markup=self.keybords.start_menu())

    def _get_current_trader(self, message):
        """
        get current trader
        :param message:
        :return: TraderUser
        """
        user = self.BD.get_user(chat_id=message.chat.id)
        return TraderUser(user.id, message.from_user.first_name)

    def handle(self):
        # обработчик(декоратор) сообщений, который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # ********** меню (выбор роли)                          **********
            if message.text == config.KEYBOARD['TRADER']:
                self._add_trader(message)
            if message.text == config.KEYBOARD['KEEPER']:
                pass
            if message.text == config.KEYBOARD['ADMIN']:
                pass

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
                self.pressed_btn_product(message,'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message,'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message,'ICE_CREAM')
            
            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.category_menu())

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            # ********** меню (Заказа)**********

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)
            
            if message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_douwn(message)
            
            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_apllay(message)
            # иные нажатия и ввод данных пользователем
            else:
                self.bot.send_message(message.chat.id,message.text)