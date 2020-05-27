from telebot.types import Update
from telegram.ext import Updater, CallbackContext

# File for recording response functions

def send_help(update: Update, context: CallbackContext):
    '''
    :param update:
    :param context:
    :return:
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text='Command list: ...')