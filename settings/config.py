import json
import os
from enum import IntEnum
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize

# название БД
NAME_DB = 'products.db'
# версия приложения
VERSION = '1.1.0'
# автор приложния
AUTHOR = 'Zveryaka A.'

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Base folder
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB) # Path to DB
INVOICES_FOLDER = 'invoices' # folder for invoices

def invoices_folder():
    invoices_path, _ = os.path.split(BASE_DIR)
    invoices_path = os.path.join(invoices_path, INVOICES_FOLDER)
    if not os.path.isdir(invoices_path):
        os.mkdir(invoices_path)
    return invoices_path

# токен выдается при регистрации приложения, храним в текстовом файле
def get_token():
    with open(os.path.join(BASE_DIR, 'token.txt'), 'r') as file:
        token, bot_name = file.readline().split(sep=';')
    return token.split(sep=' = ')[1].replace("'", '')

TOKEN = get_token()
DIALOG = 'settings/dialog'
COMPANY_INFO = 'settings/company.json'

def is_company_info():
    """
    check if company info json file exists
    :return True: if company info json file exists, False: otherwise
    """
    return os.path.exists(COMPANY_INFO)

def company_info():
    """
    get dict from company info json file
    :return info: dict of company info
    """
    with open(COMPANY_INFO, mode='r') as file_obj:
        info = json.load(file_obj)
    return info

COUNT = 0

# Keyboard buttons for common and trader user
KEYBOARD = {
    'CHOOSE_ORDER': 'Выбрать заказ',
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: TradingStore'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLY': '✅ Оформить заказ',
    'COPY': '©️',
    'TRADER': 'Trader',
    'KEEPER': 'Keeper',
    'ADMIN': 'Admin'
}

# Keyboard for administrator
ADMINISTRATIVE = {
    'MAIN': 'В начало',
    'PROPERTY': 'Реквизиты',
    'PROPERTY_CHANGE': 'Изменить',
    'PROPERTY_ADD': 'Добавить'
}

# Id ctegory to products
CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
}

# name commands
COMMANDS = {
    'START': "start",
    'HELP': "help",
}


# Roles of users
class Role(IntEnum):
    Trader = 1
    Keeper = 2
    Admin = 3


# Order's Status
class Status(IntEnum):
    New = 0
    Work = 1
    Complete = 2
    Done = 3
    Cancel = 4
    Canceled = 5


# Dialog state
class DialogState(IntEnum):
    NoDialog = 0
    CompanyName = 1
    CompanyTaxpayer = 2
    CompanyRegistrationID = 3
    CompanyAddress = 4
    CompanyPhone = 5
    CompanyEmail = 6
    BankAccountName = 7
    BankAccountID = 8
    BankAccountAccount = 9
    BankAccountCorrespondent = 10

dialog_state_name = {
    DialogState.CompanyName: 'название компании',
    DialogState.CompanyTaxpayer: 'ИНН компании',
    DialogState.CompanyRegistrationID: 'КПП компании',
    DialogState.CompanyAddress: 'адрес компании',
    DialogState.CompanyPhone: 'телефон компании',
    DialogState.CompanyEmail: 'электронный адрес компании',
    DialogState.BankAccountName: 'название банка компании',
    DialogState.BankAccountID: 'БИК банка компании',
    DialogState.BankAccountAccount: 'номер расчётного счёта комании',
    DialogState.BankAccountCorrespondent: 'номер корреспондентского счёта компании'
}