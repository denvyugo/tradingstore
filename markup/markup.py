# импортируем специальные типы телеграм бота для создания кнопок и клавиатуры
import json
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardRemove)
# импортируем настройки и утилиты
from settings import config
#  импортируем менеджер для работы с БД
from DB.DBAlchemy import DBManager
from models.order_trading import TraderUser


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки клавиатуры бота
    """
    # инициализация разметки 
    def __init__(self):
        self.markup = None
        # инициализация менеджера для работы с БД
        self.BD = DBManager()
 
    def set_btn(self, name, step='', quantity=0):
        """ 
        Создает и возвращает кнопку по входным параметрам 
        """
        if name == "AMOUNT_ORDERS":
            config.KEYBOARD["AMOUNT_ORDERS"] = step
        
        if name == "AMOUNT_PRODUCT":
            config.KEYBOARD["AMOUNT_PRODUCT"] = "{}".format(quantity)
        
        if name == "APPLY":
            # создает кнопку оформить с данными о стоимости товара округленного до 2 - го знака после запятой
            config.KEYBOARD["APPLY"] = "{}({}) руб".format('✅ Оформить', step)

        return KeyboardButton(config.KEYBOARD[name])

    def set_inline_btn(self, name, data=''):
        """ 
        Создает и возвращает инлайн кнопку по входным параметрам 
        """
        if len(data) == 0:
            data = str(name.id)
        return InlineKeyboardButton(str(name), callback_data=data)
    
    def remove_menu(self):
        """ 
        Удаляет данны кнопки и возвращает ее 
        """
        return ReplyKeyboardRemove()

    def info_menu(self):
        """ 
        Создает разметку кнопок в меню info 
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        """ 
        Создает разметку кнопок в меню settings 
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def start_menu(self):
        """ 
        Создает разметку кнопок в основном меню и возвращает разметку 
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_ORDER')
        itm_btn_2 = self.set_btn('CHOOSE_GOODS')
        itm_btn_3 = self.set_btn('INFO')
        itm_btn_4 = self.set_btn('SETTINGS')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2)
        self.markup.row(itm_btn_3, itm_btn_4)
        return self.markup

    def current_order_menu(self):
        """
        making markup for work with order
        :return:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_ORDER')
        itm_btn_2 = self.set_btn('CHOOSE_GOODS')
        itm_btn_3 = self.set_btn('<<')
        itm_btn_4 = self.set_btn('ORDER')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2)
        self.markup.row(itm_btn_3, itm_btn_4)
        return self.markup

    def category_menu(self):
        """ 
        Создает разметку кнопок в меню категорий товара и возвращает разметку 
        """
        self.markup = ReplyKeyboardMarkup(True,True,row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))
        return self.markup

    def select_role_menu(self):
        """
        markup for role selection
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        itm_btn_1 = self.set_btn('TRADER')
        itm_btn_2 = self.set_btn('KEEPER')
        itm_btn_3 = self.set_btn('ADMIN')
        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3)
        return self.markup

    def set_select_category(self, trader, category):
        """ 
        Создает разметку инлайн кнопок в выбранной категории товара и возвращает разметку 
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в название инлайн кнопок данные с БД в соответствие с категорией товара
        order_current = self.BD.get_order_current(trader_id=trader.id)
        if order_current is None:
            order_current = trader.order.save(self.BD)
        for itm in self.BD.select_all_products_category(category):
            # dump a data to json string
            # keys & values are: 'm' - menu: 'p' - products (add one product)
            #                    't' - trader id
            #                    'o' - current order id
            #                    'p' - product id
            data = json.dumps({'m': 'p',
                               't': trader.id,
                               'o': order_current.id,
                               'p': itm.id},
                              separators=(',', ':'))
            self.markup.add(self.set_inline_btn(str(itm), data))
        return self.markup

    def orders_info_menu(self, trader_user: TraderUser):
        """
        create inline-menu of trader's orders
        :param trader_user:
        :return: markup
        """
        orders = trader_user.get_orders(self.BD)
        self.markup = InlineKeyboardMarkup(row_width=1)
        if len(orders):
            for order in orders:
                # dump a data to json string
                # keys & values are: 'm' - menu: 'o' - orders (choose one order to work with)
                #                    't' - trader id
                #                    'o' - current order id
                data = json.dumps({'m': 'o',
                                   't': trader_user.id,
                                   'o': order.id},
                                  separators=(',', ':'))
                self.markup.add(self.set_inline_btn(str(order), data))
            return self.markup

    def set_select_client(self, trader: TraderUser):
        """
        set menu of list of clients
        :param trader:
        :return markup: inline buttons
        """
        clients = self.BD.get_clients()
        if len(clients):
            self.markup = InlineKeyboardMarkup(row_width=1)
            for client in clients:
                # dump a data to json string
                # keys & values are: 'm' - menu: 'c' - clients (choose one client for order)
                #                    't' - trader id
                #                    'o' - order id
                #                    'c' - client id
                data = json.dumps({'m': 'c',
                                   't': trader.id,
                                   'o': trader.order.id,
                                   'c': client.id})
                self.markup.add(self.set_inline_btn(str(client), data))
            return self.markup

    def orders_menu(self, step):
        """ 
        Создает разметку кнопок в заказе товара и возвращает разметку
        :param step: json with parameters: number, quantity, positions, total_price
        :return: markup
        """
        parameters = json.loads(step)
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X')
        itm_btn_2 = self.set_btn('DOWN')
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', quantity=parameters['quantity'])
        itm_btn_4 = self.set_btn('UP')

        itm_btn_5 = self.set_btn('BACK_STEP')
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step='{} из {}'.format(parameters['number'], parameters['positions']))
        itm_btn_7 = self.set_btn('NEXT_STEP')
        itm_btn_8 = self.set_btn('APPLY', step=parameters['total_price'])
        itm_btn_9 = self.set_btn('<<')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1,itm_btn_2,itm_btn_3,itm_btn_4)
        self.markup.row(itm_btn_5,itm_btn_6,itm_btn_7)
        self.markup.row(itm_btn_9,itm_btn_8)  

        return self.markup

    def admin_menu(self):
        """
        make admin menu
        :return markup:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn1 = KeyboardButton(config.ADMINISTRATIVE['PROPERTY'])
        itm_btn2 = KeyboardButton(config.ADMINISTRATIVE['STORE'])
        self.markup.row(itm_btn1, itm_btn2)
        return self.markup

    def company_change(self):
        """
        keyboard for company change admin's dialog
        :return markup:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn1 = KeyboardButton(config.ADMINISTRATIVE['PROPERTY_CHANGE'])
        itm_btn2 = KeyboardButton(config.ADMINISTRATIVE['MAIN'])
        self.markup.row(itm_btn1, itm_btn2)
        return self.markup

    def company_add(self):
        """
        keyboard for add new company admin's dialog
        :return markup:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn1 = KeyboardButton(config.ADMINISTRATIVE['PROPERTY_ADD'])
        itm_btn2 = KeyboardButton(config.ADMINISTRATIVE['MAIN'])
        self.markup.row(itm_btn1, itm_btn2)
        return self.markup

    def keeper_menu(self):
        """
        make keeper's main menu
        :return markup:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn1 = KeyboardButton(config.KEEPER['GET_ORDERS'])
        self.markup.row(itm_btn1)
        return self.markup

    def keeper_orders_menu(self, keeper_user, next_status):
        """
        create inline-buttons menu of orders with selected status
        :param keeper_user:
        :param next_status: status to set order if it will be selected
        :return:
        """
        orders = keeper_user.get_orders(db=self.BD)
        self.markup = InlineKeyboardMarkup(row_width=1)
        if len(orders):
            for order in orders:
                # dump a data to json string
                # keys & values are: 'm' - menu: 's' - selected orders with
                #                    keeper user defined status (choose one order to work with)
                #                    'k' - keeper id
                #                    'o' - current order id
                #                    'n' - next status
                data = json.dumps({'m': 's',
                                   'k': keeper_user.chat_id,
                                   'o': order.id,
                                   'n': next_status},
                                  separators=(',', ':'))
                self.markup.add(self.set_inline_btn(str(order), data))
            return self.markup
