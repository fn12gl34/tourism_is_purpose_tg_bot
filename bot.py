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

info_message = '''
Ребята, всем привет!

Напоминаем вам о нашем проекте - мы помогаем в адаптации в новой стране людям, которые уезжают из России

Сейчас мы активно ищем волонтеров в разных странах, которые готовы оказывать помощь уезжающим.

Как можно помочь:

- предоставить жилье на первое время или помочь его найти
- встретить от границы или помочь организовать трансфер
- проконсультировать по бытовым и организационным вопросам в разных странах
- поговорить и поддержать
- задонатить

Если вы готовы стать волонтером, заполните, пожалуйста, [форму](https://airtable.com/shrUZIxbaoV0Lyk7c). Когда появится запрос, помочь в котором сможете именно вы, куратор напишет вам в тг и свяжет вас с эвакуантом

Если вам или вашим близким нужна помощь, заполните, пожалуйста, эту [форму](https://airtable.com/shrUWtxaCUGaXzCjq). 
Наш куратор свяжется с вами, ответит на ваши вопросы и свяжет с волонтером из той страны, в которую вы собираетесь релоцироваться

Также у нас есть [гайд](https://www.notion.so/b3f5058775464ccb8b7896a78fe57b54) по разным странам, который мы активно пополняем информацией. Надеемся, он вам поможет

Распространяйте информацию о нас среди друзей, давайте помогать вместе 🤍
'''

def send_info_msg_to_chat():
    bot.send_message(CHAT_ID, info_message, parse_mode='MarkdownV2')


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
        schedule.every(1).minutes.do(send_info_msg_to_chat)
        ScheduleMessage.start_process() 
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
