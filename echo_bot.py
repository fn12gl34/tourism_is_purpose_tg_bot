import os
import telebot

TG_BOT_APIKEY = os.getenv('TG_BOT_APIKEY') 

bot = telebot.TeleBot(TG_BOT_APIKEY, parse_mode=None)

@bot.message_handler(content_types=['new_chat_members'])
def remove_info(message):
    bot.delete_message(message.chat.id, message.message_id)


bot.infinity_polling()

