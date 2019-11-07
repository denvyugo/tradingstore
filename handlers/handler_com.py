# импортируем класс родитель
from handlers.handler import Handler
from settings.config import Role

class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start, /help и тп...
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        обрабатывает входящие /start команды
        """
        # get user if exist
        user = self.BD.get_user(chat_id=message.chat.id)
        reply = ''
        markup = None
        if user is None:
            reply = '{}, здравствуйте! Укажите, пожалуйста, Вашу должность.'
            markup = self.keybords.select_role_menu()
        elif user.role == Role.Trader:
            reply = '{}, здравствуйте! Жду дальнейших задач.'
            markup = self.keybords.start_menu()
        elif user.role == Role.Admin:
            reply = '{}, здравствуйте! Жду дальнейших задач.'
            markup = self.keybords.admin_menu()
        elif user.role == Role.Keeper:
            reply = '{}, здравствуйте! Жду дальнейших задач.'
            markup = self.keybords.keeper_menu()
        self.bot.send_message(message.chat.id,
                              reply.format(message.from_user.first_name),
                              reply_markup=markup)

    def handle(self):
        # обработчик(декоратор) сообщений, который обрабатывает входящие /start команды.
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
