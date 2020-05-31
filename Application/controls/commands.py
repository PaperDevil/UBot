import os
import sys
import logging

from deeppavlov import train_model
from deeppavlov.deprecated.agents.default_agent import DefaultAgent
from deeppavlov.deprecated.agents.processors import HighestConfidenceSelector
from deeppavlov.deprecated.skills.pattern_matching_skill import PatternMatchingSkill
from telebot.types import Update
from telegram.ext import Updater, CallbackContext


# File for recording response functions

QAModel = train_model(os.path.dirname(sys.argv[0]) + "/Application/config.json")
agent = DefaultAgent([QAModel], skills_selector=HighestConfidenceSelector())

def send_help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Command list: ...')

def QAnswer(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=agent([update.message.text])[0])

def get_indicates(update: Update, context: CallbackContext):
    ...

def register_user(update: Update, context: CallbackContext):
    ...

def get_personal_account(update: Update, context: CallbackContext):
    ...