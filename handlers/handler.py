# импортируем библиотеку абстрактный класс
import abc
# импортируем разметку клавиатуры и клавиш
from markup.markup import Keyboards
# импортируем менеджер для работы с библиотекой
from DB.DBAlchemy import DBManager


class Handler(metaclass=abc.ABCMeta):
    """
    Абстрактный класс патерна Chain of responsibility
    """
    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot
        # инициализируем разметку кнопок в меню и экрана
        self.keybords = Keyboards()
        # инициализация менеджера для работы с БД
        self.BD = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass