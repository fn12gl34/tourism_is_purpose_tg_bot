import os
import time
from multiprocessing.context import Process

from flask import Flask, request
import telebot
import schedule

TOKEN = os.getenv('TG_BOT_APIKEY')
CHAT_ID = os.getenv('CHAT_ID')
APP_URL = os.getenv('APP_URL')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

def send_msg_to_chat():
    bot.send_message(CHAT_ID, 'hello there')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL + TOKEN)
    return '!', 200


@bot.message_handler(content_types=['new_chat_members'])
def remove_info(message):
    bot.delete_message(message.chat.id, message.message_id)
    
    
class ScheduleMessage:
    def send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(10)
            
    def start_process():
        p = Process(target=ScheduleMessage.send_schedule, args=())
        p.start()

if __name__ == '__main__':
    if CHAT_ID:
        schedule.every(1).minutes.do(send_msg_to_chat)
        ScheduleMessage.start_process() 
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))