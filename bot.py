import os
import time
from multiprocessing.context import Process

from flask import Flask, request
import telebot
from telebot.types import ChatPermissions
import schedule

TOKEN = os.getenv('TG_BOT_APIKEY')
CHAT_ID = os.getenv('CHAT_ID')
TEST_CHAT_ID = os.getenv('TEST_CHAT_ID')
APP_URL = os.getenv('APP_URL')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


restrict_message = '''
Ребята, мы включаем медленный режим на ночь, вы сможете отправлять сообщения только раз в час\\. Это необходимо, чтобы ночью в чате не было флуда и наш модератор, который работает ночью, смог контролировать весь поток сообщений\\. Поэтому старайтесь формулировать весь свой запрос и вопросы в одно сообщение
 
В 8 утра по Мск\\. общение в чате перейдет в обычный режим и вы сможете активнее общаться

Также напоминаем вам правила чата:
\\- не флудить
\\- не грубить другими участникам
\\- не кидать информацию, в которой вы не уверены \\(постарайтесь проверить ее правдивость перед тем, как шерить с окружающими\\)
\\- прежде, чем задать вопрос, нужно поискать ответ в нашем [гайде](https://www.notion.so/b3f5058775464ccb8b7896a78fe57b54), чате и в закрепах 

Не игнорируйте их, пожалуйста, и будьте бережны друг к другу\\! Доброй ночи🤍
'''

unrestrict_message = '''
Ребят, медленный режим в чате выключен, теперь вы можете активно общаться

Обменивайтесь информацией, помогайте друг другу и будьте бережны к окружающим

Напоминаем вам правила чата:
\\- не флудить
\\- не грубить другими участникам
\\- не кидать информацию, в которой вы не уверены \\(постарайтесь проверить ее правдивость перед тем, как шерить с окружающими\\)
\\- прежде, чем задать вопрос, нужно поискать ответ в нашем гайде, чате и в закрепах 

Хорошего вам дня\\! 🤍
'''

info_message = '''
Ребята, всем привет\\!

Напоминаем вам о нашем проекте \\- мы помогаем в адаптации в новой стране людям, которые уезжают из России

Сейчас мы активно ищем волонтеров в разных странах, которые готовы оказывать помощь уезжающим\\.

Как можно помочь:

\\- предоставить жилье на первое время или помочь его найти
\\- встретить от границы или помочь организовать трансфер
\\- проконсультировать по бытовым и организационным вопросам в разных странах
\\- поговорить и поддержать
\\- задонатить

Если вы готовы стать волонтером, заполните, пожалуйста, [форму](https://airtable.com/shrUZIxbaoV0Lyk7c)\\. Когда появится запрос, помочь в котором сможете именно вы, куратор напишет вам в тг и свяжет вас с эвакуантом

Если вам или вашим близким нужна помощь, заполните, пожалуйста, эту [форму](https://airtable.com/shrUWtxaCUGaXzCjq)\\. 
Наш куратор свяжется с вами, ответит на ваши вопросы и свяжет с волонтером из той страны, в которую вы собираетесь релоцироваться

Также у нас есть [гайд](https://www.notion.so/b3f5058775464ccb8b7896a78fe57b54) по разным странам, который мы активно пополняем информацией\\. Надеемся, он вам поможет

Распространяйте информацию о нас среди друзей, давайте помогать вместе\\! 🤍
'''

def send_info_msg_to_chat():
    bot.send_message(CHAT_ID, info_message, parse_mode='MarkdownV2', disable_web_page_preview=True)
    
    
def restrict_chat_settings():
    bot.send_message(TEST_CHAT_ID, restrict_message, parse_mode='MarkdownV2', disable_web_page_preview=True)
    chp = ChatPermissions(can_send_messages=False)
    bot.set_chat_permissions(TEST_CHAT_ID, permissions=chp)
    
    
def unrestrict_chat_settings():
    bot.send_message(TEST_CHAT_ID, unrestrict_message, parse_mode='MarkdownV2', disable_web_page_preview=True)
    chp = ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_invite_users=True, can_add_web_page_previews=True)
    bot.set_chat_permissions(TEST_CHAT_ID, permissions=chp)
    

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
        if TEST_CHAT_ID:
            schedule.every(2).minutes.do(restrict_chat_settings)
            schedule.every(4).minutes.do(unrestrict_chat_settings)
        schedule.every().day.at('09:00').do(send_info_msg_to_chat)
        ScheduleMessage.start_process() 
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
