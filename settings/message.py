# импортируем настройки для отражения эмоджи
from .config import KEYBOARD,VERSION,AUTHOR

# ответ пользователю при почещении trading_store
trading_store = """

<b>Добро пожаловать в приложение
            TradingStore !!!</b>

Данное приложение разработано 
специально для торговых представителей,
далее <i>(ТП/СВ)</i>,а также для кладовщиков, 
коммерческих организаций осуществляющих
оптово-розничную торговлю.

ТП используя приложение TradingStore,
в удобной интуитивной форме смогут без
особого труда принять заказ от клиента.
TradingStore поможет сформировать заказ
и в удобном виде адресует кладовщику 
фирмы для дальнейшего комплектования заказа. 

"""
# ответ пользователю при почещении settings
settings = """
<b>Общее руководство приложением:</b>

<i>Навигация:</i>

-<b>({}) - </b><i>назад</i>
-<b>({}) - </b><i>вперед</i>
-<b>({}) - </b><i>увеличить</i>
-<b>({}) - </b><i>уменьшить</i>
-<b>({}) - </b><i>следующий</i>
-<b>({}) - </b><i>предыдующий</i>

<i>Специальные кнопки:</i>

-<b>({}) - </b><i>удалить</i>
-<b>({}) - </b><i>заказ</i>
-<b>({}) - </b><i>Оформить заказ</i>

<i>Общая информация:</i>

-<b>версия программы: - </b><i>({})</i>
-<b>разработчик: - </b><i>({})</i>


<b>{}GeekBrains 2019</b>

""".format(
    KEYBOARD['<<'],
    KEYBOARD['>>'],
    KEYBOARD['UP'],
    KEYBOARD['DOWN'],
    KEYBOARD['NEXT_STEP'],
    KEYBOARD['BACK_STEP'],
    KEYBOARD['X'],
    KEYBOARD['ORDER'],
    KEYBOARD['APPLY'],
    VERSION,
    AUTHOR,
    KEYBOARD['COPY'],
)
# ответ пользователю при почещении product_order
product_order = """
Выбранный товар:

{}
{}
Стоимость: {} руб

добавлен в заказ!!!

На складе осталось {} ед. 
"""
# ответ пользователю при почещении order
order = """

<i>Название:</i> <b>{}</b>

<i>Описание:</i> <b>{}</b>

<i>Стоимость:</i> <b>{} руб за 1 ед.</b>

<i>Количество позиций:</i> <b>{} ед.</b> 
"""

order_number = """

<b>Позиция в заказе № </b> <i>{}</i>

"""
# ответ пользователю при почещении no_orders
no_orders = """
<b>Заказ отсутствует !!!</b>
"""
# ответ пользователю при почещении apply
apply = """
<b>Ваш заказ оформлен !!!</b>

<i>Общая стоимость заказа составляет:</i> <b>{} руб</b>

<i>Общее количество позиций составляет:</i> <b>{} ед.</b>

<b>ЗАКАЗ НАПРАВЛЕН НА СКЛАД,
ДЛЯ ЕГО КОМПЛЕКТОВКИ !!!</b>
"""
# словарь ответов пользователю
MESSAGES = {
    'trading_store': trading_store,
    'product_order': product_order,
    'order': order,
    'order_number': order_number,
    'no_orders': no_orders,
    'apply': apply,
    'settings': settings
}