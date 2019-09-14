import os
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize

def get_token():
    with open(os.path.join(BASE_DIR, 'token.txt'), 'r') as file:
        token, bot_name = file.readline().split(sep=';')
    return token.split(sep=' = ')[1]

# название БД
NAME_DB = 'products.db'
# версия приложения
VERSION = '1.1.0'
# автор приложния
AUTHOR = 'Zveryaka A.'

# Base folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
# Path to DB
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)

# токен выдается при регистрации приложения
TOKEN = get_token()

COUNT = 0

# Keyboard buttons
KEYBOARD = {
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
    'DOUWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️'

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
