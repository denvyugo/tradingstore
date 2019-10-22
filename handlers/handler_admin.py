import json
import shelve
# импортируем настройки и утилиты
from settings import config
# импортируем ответ пользователю
from settings.message import MESSAGES
# импортируем класс родитель
from handlers.handler import Handler
from models.admin import Admin


class HandlerAdmin(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def handle(self):
        @self.bot.message_handler(func=lambda message: message.text == config.ADMINISTRATIVE['PROPERTY'])
        def check_property(message):
            """
            check if company info json file exists
            :param message:
            :return markup: with change button if company info json file exists
                            with add button if company info json file not exists
            """
            admin = Admin(chat_id=message.chat.id)
            if config.is_company_info():
                info = config.company_info()
                admin.set_company_info(company_info=info)
                reply = MESSAGES['company_info'].format(info['name'], info['taxpayerID'], info['registrationID'],
                                                        info['address'], info['phone'], info['email'],
                                                        info['bank_account']['name'], info['bank_account']['id'],
                                                        info['bank_account']['account'],
                                                        info['bank_account']['corr_acc'])
                markup = self.keybords.company_change()
            else:
                reply = MESSAGES['no_company']
                markup = self.keybords.company_add()
            admin.dialog_status=config.DialogState.NoDialog
            self.bot.send_message(message.chat.id, reply, parse_mode='HTML', reply_markup=markup)

        @self.bot.message_handler(func=lambda message: _start_dialog_property(message.text))
        def start_dialog_property(message):
            """
            add to shelve status
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            company = admin.get_company_name()
            if len(company):
                reply = '<b>Компания:</b> {}<br>Введите другое название, чтобы изменить:'.format(company)
            else:
                reply = 'Введите название Вашей компании:'
            admin.dialog_status=config.DialogState.CompanyName
            self.bot.send_message(message.chat.id, reply, parse_mode='HTML')

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) == config.DialogState.CompanyName)
        def input_company_name(message):
            """
            input company name
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_name(message.text):
                reply = 'Компания: {}'.format(message.text)
                admin.dialog_status = config.DialogState.CompanyTaxpayer
            else:
                reply = 'Повторите, пожалуйста ввод'
            self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) == \
                                                       config.DialogState.CompanyTaxpayer)
        def input_company_name(message):
            """
            input company name
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_name(message.text):
                reply = 'Компания: {}'.format(message.text)
                admin.dialog_status = config.DialogState.CompanyTaxpayer
            else:
                reply = 'Повторите, пожалуйста ввод'
            self.bot.send_message(message.chat.id, reply)

        def _start_dialog_property(message):
            """
            if administrator tap PROPERTY CHANGE or PROPERTY ADD button, then start dialog
            :param message:
            :return True: if change or add property, False: otherwise
            """
            return message == config.ADMINISTRATIVE['PROPERTY_CHANGE'] or \
                   message == config.ADMINISTRATIVE['PROPERTY_ADD']

        def _dialog_state(chat_id):
            """
            get status dialog from admin
            :param chat_id:
            :return dialog_status:
            """
            admin = Admin(chat_id=chat_id)
            return admin.dialog_status