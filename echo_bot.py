import os
import time
import telebot
import flask

TG_BOT_APIKEY = os.getenv('TG_BOT_APIKEY') 

WEBHOOK_HOST = 'https://tourism-is-purpose-tg-bot.herokuapp.com/'
WEBHOOK_PORT = os.environ.get('PORT', 80)  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0' 

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TG_BOT_APIKEY)

bot = telebot.TeleBot(TG_BOT_APIKEY, parse_mode=None)
app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(content_types=['new_chat_members'])
def remove_info(message):
    bot.delete_message(message.chat.id, message.message_id)

    
bot.remove_webhook()

time.sleep(0.1)

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app.run(host=WEBHOOK_LISTEN, port=WEBHOOK_PORT)
