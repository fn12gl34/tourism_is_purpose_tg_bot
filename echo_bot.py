import os
import telebot
from flask import Flask, request

TG_BOT_APIKEY = os.getenv('TG_BOT_APIKEY') 

bot = telebot.TeleBot(TG_BOT_APIKEY, parse_mode=None)
server = Flask('tourism_is_purpose_tg_bot')


@bot.message_handler(content_types=['new_chat_members'])
def remove_info(message):
    bot.delete_message(message.chat.id, message.message_id)
    
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://tourism-is-purpose-tg-bot.herokuapp.com/') # этот url нужно заменить на url вашего Хероку приложения
    return '?', 200
    
server.run(host='0.0.0.0', port=os.environ.get('PORT', 80))
