# импортируем настройки и утилиты
from settings.config import (ADMINISTRATIVE, DialogState, dialog_state_name,
                             is_company_info, company_info, Role)
# импортируем ответ пользователю
from settings.message import MESSAGES
# импортируем класс родитель
from handlers.handler import Handler
from models.admin import Admin


class HandlerAdmin(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def handle(self):
        @self.bot.message_handler(func=lambda message: message.text == ADMINISTRATIVE['PROPERTY'])
        def check_property(message):
            """
            check if company info json file exists
            :param message:
            :return markup: with change button if company info json file exists
                            with add button if company info json file not exists
            """
            admin = Admin(chat_id=message.chat.id)
            if is_company_info():
                info = company_info()
                admin.set_company_info(company_info=info)
                admin.dialog_type = True
                reply = _format_company_info_mes(info)
                markup = self.keybords.company_change()
            else:
                admin.dialog_type = False
                reply = MESSAGES['no_company']
                markup = self.keybords.company_add()
            admin.dialog_status = DialogState.NoDialog
            self.bot.send_message(message.chat.id, reply, parse_mode='HTML', reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text == ADMINISTRATIVE['STORE'])
        def check_store(message):
            """
            check if store info is present in database than get it
            and try to change - set dialog type True,
            otherwise: try to add a new store info - set dialog type False
            :param message:
            :return:
            """
            # TODO: implement method to start dialog about store information

        @self.bot.message_handler(func=lambda message: message.text == ADMINISTRATIVE['MAIN'])
        def admin_main(message):
            """
            intro to main admin menu
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            admin.dialog_status = DialogState.NoDialog
            self.bot.send_message(message.chat.id, 'Главное меню',
                                  reply_markup=self.keybords.admin_menu())

        def _format_company_info_mes(info):
            """
            format company info message
            :param info:
            :return message:
            """
            return  MESSAGES['company_info'].format(info['name'], info['taxpayerID'],
                                                    info['registrationID'],
                                                    info['address'], info['phone'],
                                                    info['email'], info['bank_account']['name'],
                                                    info['bank_account']['id'],
                                                    info['bank_account']['account'],
                                                    info['bank_account']['corr_acc'])

        @self.bot.message_handler(func=lambda message: _start_dialog_property(message.text))
        def start_dialog_property(message):
            """
            add to shelve status
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.dialog_type:
                company = admin.get_company_name()
                _send_current_value(admin.chat_id, DialogState.CompanyName, company)
            _change_dialog_state(admin, DialogState.CompanyName)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.CompanyName)
        def input_company_name(message):
            """
            input company name
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_name(message.text):
                if admin.dialog_type:
                    value = admin.get_company_taxpayer()
                    _send_current_value(admin.chat_id, DialogState.CompanyTaxpayer, value)
                _change_dialog_state(admin, DialogState.CompanyTaxpayer)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.CompanyTaxpayer)
        def input_company_taxpayer(message):
            """
            input company taxpayer ID
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_taxpayer(message.text):
                if admin.dialog_type:
                    value = admin.get_company_registry()
                    _send_current_value(admin.chat_id, DialogState.CompanyRegistrationID, value)
                _change_dialog_state(admin, DialogState.CompanyRegistrationID)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.CompanyRegistrationID)
        def input_company_registration(message):
            """
            input company registration ID
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_registry(message.text):
                if admin.dialog_type:
                    value = admin.get_company_address()
                    _send_current_value(admin.chat_id, DialogState.CompanyAddress, value)
                _change_dialog_state(admin, DialogState.CompanyAddress)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.CompanyAddress)
        def input_company_address(message):
            """
            input company address
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_address(message.text):
                if admin.dialog_type:
                    value = admin.get_company_phone()
                    _send_current_value(admin.chat_id, DialogState.CompanyPhone, value)
                _change_dialog_state(admin, DialogState.CompanyPhone)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(
            func=lambda message: _dialog_state(message.chat.id) == DialogState.CompanyPhone)
        def input_company_phone(message):
            """
            input company phone
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_phone(message.text):
                if admin.dialog_type:
                    value = admin.get_company_email()
                    _send_current_value(admin.chat_id, DialogState.CompanyEmail, value)
                _change_dialog_state(admin, DialogState.CompanyEmail)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.CompanyEmail)
        def input_company_email(message):
            """
            input company email
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_company_email(message.text):
                if admin.dialog_type:
                    value = admin.get_bank_name()
                    _send_current_value(admin.chat_id, DialogState.BankAccountName, value)
                _change_dialog_state(admin, DialogState.BankAccountName)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.BankAccountName)
        def input_bank_name(message):
            """
            input company bank name
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_bank_name(message.text):
                if admin.dialog_type:
                    value = admin.get_bank_id()
                    _send_current_value(admin.chat_id, DialogState.BankAccountID, value)
                _change_dialog_state(admin, DialogState.BankAccountID)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.BankAccountID)
        def input_bank_id(message):
            """
            input company bank id
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_bank_id(message.text):
                if admin.dialog_type:
                    value = admin.get_bank_account()
                    _send_current_value(admin.chat_id, DialogState.BankAccountAccount, value)
                _change_dialog_state(admin, DialogState.BankAccountAccount)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.BankAccountAccount)
        def input_bank_account(message):
            """
            input company bank account
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_bank_account(message.text):
                if admin.dialog_type:
                    value = admin.get_bank_corr()
                    _send_current_value(admin.chat_id, DialogState.BankAccountCorrespondent, value)
                _change_dialog_state(admin, DialogState.BankAccountCorrespondent)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        @self.bot.message_handler(func=lambda message: _dialog_state(message.chat.id) ==
                                  DialogState.BankAccountCorrespondent)
        def input_bank_corr(message):
            """
            input company bank correspondent account
            :param message:
            :return:
            """
            admin = Admin(chat_id=message.chat.id)
            if admin.set_bank_corr(message.text):
                admin.dialog_info_save()
                _change_dialog_state(admin, DialogState.NoDialog)
                info = company_info()
                reply = _format_company_info_mes(info)
                markup = self.keybords.company_change()
                self.bot.send_message(message.chat.id, reply,
                                      parse_mode='HTML', reply_markup=markup)
            else:
                reply = 'Повторите, пожалуйста ввод'
                self.bot.send_message(message.chat.id, reply)

        def _start_dialog_property(message):
            """
            if administrator tap PROPERTY CHANGE or PROPERTY ADD button, then start dialog
            :param message:
            :return True: if change or add property, False: otherwise
            """
            return message in (ADMINISTRATIVE['PROPERTY_CHANGE'],
                               ADMINISTRATIVE['PROPERTY_ADD'])

        def _dialog_state(chat_id):
            """
            get status dialog from admin
            :param chat_id:
            :return dialog_status:
            """
            user = self.BD.get_user(chat_id=chat_id)
            if not user is None:
                if user.role == Role.Admin:
                    admin = Admin(chat_id=chat_id)
                    return admin.dialog_status

        def _change_dialog_state(admin, state):
            admin.dialog_status = state
            if state in dialog_state_name:
                reply = '<b>Укажите {}:</b>'.format(dialog_state_name[state])
                self.bot.send_message(admin.chat_id, reply, parse_mode='HTML')

        def _send_current_value(chat_id, state, value):
            """
            send current value of parameter to change
            :param state:
            :param value:
            :return:
            """
            if len(value):
                reply = '<b>{}:</b> {}'.format(dialog_state_name[state], value)
                self.bot.send_message(chat_id, reply, parse_mode='HTML')
