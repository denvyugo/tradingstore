# импортируем класс родитель
from handlers.handler import Handler

class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /startи /help и тп...
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        обрабатывает входящие /start команды
        """
        self.bot.send_message(message.chat.id,
                              message.from_user.first_name + ', здравствуйте! Жду дальнейших задач.',
                              reply_markup=self.keybords.start_menu())

    def handle(self):
        # обработчик(декоратор) сообщений, который обрабатывает входящие /start команды.
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)