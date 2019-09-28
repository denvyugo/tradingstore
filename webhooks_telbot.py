import logging
import cherrypy
import telebot
from settings import config
from handlers.handler_main import HandlerMain

API_TOKEN = '<api_token>'

WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

class TelBot:
    """
    Основной класс телеграмм бота(Сервер), в основе которого 
    используется библиотека pyTelegramBotAPI
    """
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        """
        Инициализация бота(Сервера)
        """
	logger = telebot.logger

	telebot.logger.setLevel(logging.INFO)
        # Получение токена
        self.token = config.TOKEN
        # Инициализация бота на основе зарегистрированного токена
        self.bot = telebot.TeleBot(self.token)
        # Инициализация оброботчика событий
        self.handler = HandlerMain(self.bot)
    
    class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

    bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
	        certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Disable CherryPy requests log
access_log = cherrypy.log.access_log
for handler in tuple(access_log.handlers):
    access_log.removeHandler(handler)

# Start cherrypy server
cherrypy.config.update({
    'server.socket_host'    : WEBHOOK_LISTEN,
    'server.socket_port'    : WEBHOOK_PORT,
    'server.ssl_module'     : 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

