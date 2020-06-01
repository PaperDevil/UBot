import os
import sys
import logging

from deeppavlov import train_model
from deeppavlov.deprecated.agents.default_agent import DefaultAgent
from deeppavlov.deprecated.agents.processors import HighestConfidenceSelector
from deeppavlov.deprecated.skills.pattern_matching_skill import PatternMatchingSkill
from telebot.types import Update
from telegram.ext import Updater, CallbackContext

from Application.controls.misc.user_commands import register, indicates, account
from Application.models.models import *

# Файл содержит функции колбэка для принимаемых ботом команд.
# Дополнительный функционал (не вызываемый командами) вынесен
# в папку ./misc

QAModel = train_model(os.path.dirname(sys.argv[0]) + "/Application/config.json")
# Путь для конфига фиксирован (hardcode), можно воспользоваться переменной окружения
agent = DefaultAgent([QAModel], skills_selector=HighestConfidenceSelector())
# Агент чисто для удобства, можно от него избавиться, если не использовать скиллы


def send_help(update: Update, context: CallbackContext):
    """
    В случае необходимости (при отладке) можно изменить функцию
    добавив ассоциативный массив доступных команд. (удобное решение)
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Доступные команды:"
                                  "\n - /help для вызова списка команд."
                                  "\n - /indicates для подачи показаний счётчика."
                                  "\n - /register для регистрации."
                                  "\n - /account для привязки лицевого счёта")


def stop(update: Update, context: CallbackContext):
    """
    Останавливает выполнение текущего контекста
    из (registration, getting_indicates, getting_account)
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Действие {context.user_data['status']} отменено.")
    context.user_data["status"] = None


def status(update: Update, context: CallbackContext):
    """
    Сообщает о выполняющемся сейчас контексте
    из (registration, getting_indicates, getting_account)
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"status is {context.user_data['status']}")

def QAnswer(update: Update, context: CallbackContext):
    """
    Обработка любой строки не являющейся командой через натренированную
    по входным данным конфига модель. Возвращает результат подстановки из
    таблиц QADatas.
    При выполнении контекста передаёт управление функции выполняющей
    соответствующую операцию.
    """
    try: context.user_data["status"]
    except: context.user_data["status"] = None
    if context.user_data["status"] == "getting_indicates":
        indicates(update, context)
    elif context.user_data["status"] == "registering":
        register(update, context)
    elif context.user_data["status"] == "getting_account":
        account(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=agent([update.message.text])[0])


def get_indicates(update: Update, context: CallbackContext):
    """
    Команда для вызова записи показаний счётчика.
    Предварительно запросит регистрацию и лицевой счёт.
    """
    try:
        with db.atomic():
            user = User.get(User.username == update.message.from_user['username'])
            if user.agent is None:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Вам всё ещё необходимо указать ваш лицевой счёт!"
                                              "Воспользуйтесь командой /account, чтобы его указать.")
                return
        context.user_data["status"] = "getting_indicates"  # Статус нужен, чтобы понимать на каком этапе пользователь
        context.user_data["indicates"] = {
            "h_kitchen": None,
            "c_kitchen": None,
            "h_bathroom": None,
            "c_bathroom": None,
            "electricity": None
        }
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="По очереди вводите показания в таком порядке:"
                                      "\n - Горячая вода - кухня,"
                                      "\n - Холодная вода - кухня,"
                                      "\n - Горячая вода - ванная,"
                                      "\n - Холодная вода - ванная,"
                                      "\n - Электроэнергия.")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Перед тем, как подавать показания счётчиков вам необходимо пройти регистрацию"
                                      "\n Воспользуйтесь командой /register, чтобы зарегистрироваться.")


def register_user(update: Update, context: CallbackContext):
    try:
        with db.atomic():
            user = User.get(User.username == update.message.from_user['username'])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Вы уже зарегистрированы! Не пытайтесь меня обмануть... Ваш идентификатор - {user.id}")
    except:
        context.user_data["status"] = "registering"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Для регистрации мне понадобится записать ваш номер телефона, отправьте мне его в виде +7 (xxx) ...")


def get_personal_account(update: Update, context: CallbackContext):
    """
    Запос на запись лицевого счёта. Входной параметр - строка из цифр.
    """
    try:
        with db.atomic():
            user = User.get(User.username == update.message.from_user['username'])
            if user.agent is None:
                context.user_data["status"] = "getting_account"
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Укажите ваш лицевой счёт, чтобы я сохранил его в базе данных.")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Для этого аккаунта уже указан лицевой счёт. "
                                              "Если вы хотите сменить лицевой счёт, воспользуйтесь командой /change_account")
    except Exception as ex:
        logger = logging.getLogger("root")
        logger.error(f"DataBaseError: {ex}")
