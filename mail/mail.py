import os

import email
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
# загружает переменные окружения из файла .env
load_dotenv()


class BotMail():
    """
    Класс BotMail, предназначен для формирования и отправки писем
    с вложенными файлами. Для отправки писем использует действующий
    аккаунт GMAIL. Все настройки подгружаются с переменного окружения
    из файла .env
    """

    def __init__(self):
        self.__sender_email = os.getenv('SENDER_EMAIL')
        self.__password_email = os.getenv('PASSWORD_EMAIL')
        self.__host_email = os.getenv('HOST_EMAIL')
        self.__port_email = os.getenv('PORT_EMAIL')
        self._message = MIMEMultipart()

    def load_file(self, filename):
        """
        Загрузка файла (PDF) в бинарном режиме
        """
        with open(filename, "rb") as attachment:
            # Заголовок письма application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Шифровка файла под ASCII символы для отправки по почте
        encoders.encode_base64(part)

        # Внесение заголовка в виде пара/ключ к части вложения
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        return part

    def set_mail(self, subject, body_text, receiver_email, filename):
        """
        Составляет письмо
        """
        self._message["Subject"] = subject
        self._message["From"] = self.__sender_email
        self._message["To"] = receiver_email

        # Сделать их текстовыми\html объектами MIMEText
        part1 = MIMEText(body_text, "plain")
        part2 = self.load_file(filename)

        # Внесение тела письма и вложение
        self._message.attach(part1)
        self._message.attach(part2)

    def send_mail(self, subject, body_text, receiver_email, filename):
        """
        Отправка письма с вложением
        """
        # Составляет письмо перед отправкой
        self.set_mail(subject, body_text, receiver_email, filename)
        # Подключение к серверу при помощи безопасного контекста и отправка письма
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(self.__host_email, self.__port_email, context=context) as server:

            server.login(self.__sender_email,
                         self.__password_email)

            server.sendmail(self.__sender_email,
                            receiver_email,
                            self._message.as_string())


# if __name__ == '__main__':
#     subject = "Письмо с PDF вложением из Python"
#     body = "Это письмо из Python с прикрепленным файлом."
#     receiver_email = "some mail"
#     filename = "some file"  # В той же папке что и код

#     mail = BotMail()
#     mail.send_mail(subject, body, receiver_email, filename)
