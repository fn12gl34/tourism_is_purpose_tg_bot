import os

from flask import Flask, request
import telebot

TOKEN = os.getenv('TG_BOT_APIKEY') 
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://tourism-is-purpose-tg-bot.herokuapp.com/' + TOKEN)
    return '!', 200


@bot.message_handler(content_types=['new_chat_members'])
def remove_info(message):
    bot.delete_message(message.chat.id, message.message_id)

    
server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
