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
        token, _ = file.readline().split(sep=';')
    return token.split(sep=' = ')[1].replace("'", '')

def get_email_config():
    email_config = {}
    with open(os.path.join(BASE_DIR, '.env'), 'r') as file:
        for line in file:
            key, value = line.split(sep=' = ')
            email_config[key] = value.replace('\n', '')
    return email_config

TOKEN = get_token()
DIALOG = os.path.join(BASE_DIR, 'dialog')
COMPANY_INFO = os.path.join(BASE_DIR, 'company.json')

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
    'COPY': '©️'
}
# Keyboard for default user (get role)
DEFAULT = {
    'TRADER': 'Trader',
    'KEEPER': 'Keeper',
    'ADMIN': 'Admin'
}

# Keyboard for keeper
KEEPER = {
    'GET_ORDERS': 'Список заказов'
}

# Keyboard for administrator
ADMINISTRATIVE = {
    'MAIN': 'В начало',
    'PROPERTY': 'Реквизиты',
    'STORE': 'Склад',
    'PROPERTY_CHANGE': 'Изменить',
    'PROPERTY_ADD': 'Добавить'
}

# Id category to products
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

# hash for default password for each roles
DEFAULT_TRADER = b'e6abfb67407de540f6e9385892fe20f35d56c47ef5bcf9aae8b12b1f6b7078d1'
DEFAULT_KEEPER = b'21c0e9cd6dd58086d61d9682524d47b933ded967c99a61eb5321e2ebd4439319'
DEFAULT_ADMIN = b'd29451272bec641a9a9628742a8629e877a551220a2c839b7d43398d2c370ffa'

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
    StoreAddress = 11
    StoreLongitude = 12
    StoreLatitude = 13
    StoreTitle = 14
    StoreDeliveryPrice = 15
    UserTrader = 16
    UserKeeper = 17
    UserAdmin = 18

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
    DialogState.BankAccountCorrespondent: 'номер корреспондентского счёта компании',
    DialogState.StoreAddress: 'адрес склада',
    DialogState.StoreLongitude: 'долгота (координаты склада)',
    DialogState.StoreLatitude: 'широта (координаты склада)',
    DialogState.StoreTitle: 'название склада',
    DialogState.StoreDeliveryPrice: 'стоимость доставки за км',
    DialogState.UserTrader: 'пароль для торгового представителя',
    DialogState.UserKeeper: 'пароль для работника склада',
    DialogState.UserAdmin: 'пароль для администратора'
}
