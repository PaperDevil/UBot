from Application.models.models import *

# Обёрточные функции для обработки данных из БД


def register(update, context):
    try:
        with db.atomic():
            user = User.create(
                username=update.message.from_user['username'],
                phone=update.message.text
            )
            user.save()
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Вы успешно зарегистрировались! Ваш идентификатор - {user.id}")
            context.user_data["status"] = None
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Извините! Произошла ошибка, при попытке регистрации. Повторите попытку позже.")
        context.user_data["status"] = None


def indicates(update, context):
    """
    Запись показаний, на входе (update.message.text) 5 сообщений
    с показаниями в виде строки цифр
    :param update:
    :param context:
    :return:
    """
    try:
        with db.atomic():
            for indicate, val in context.user_data["indicates"].items():
                if context.user_data["indicates"][indicate] is None:
                    context.user_data["indicates"][indicate] = update.message.text
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=f"{indicate}:{update.message.text}")
                    break
            if context.user_data["indicates"]["electricity"] is not None:
                context.user_data["status"] = None
                indicates = Indicate.create(
                    account_id=User.get(User.username == update.message.from_user['username']),
                    date=datetime.now(),
                    h_kitchen=context.user_data["indicates"]['h_kitchen'],
                    c_kitchen=context.user_data["indicates"]['c_kitchen'],
                    h_bathroom=context.user_data["indicates"]['h_bathroom'],
                    c_bathroom=context.user_data["indicates"]['c_bathroom'],
                    electricity=context.user_data["indicates"]['electricity']
                )
                indicates.save()
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Вы успешно подали показания:" +
                                              f"\n Горячая вода, кухня - {context.user_data['indicates']['h_kitchen']};" +
                                              f"\n Холодная вода, кухня - {context.user_data['indicates']['c_kitchen']};" +
                                              f"\n Горячая вода, ванная - {context.user_data['indicates']['h_bathroom']};" +
                                              f"\n Холодная вода, ванная - {context.user_data['indicates']['c_bathroom']};" +
                                              f"\n Электроэнергия - {context.user_data['indicates']['electricity']}.")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Извините! Произошла ошибка, при попытке записи показаний." +
                                      "Повторите попытку позже.")
        context.user_data["status"] = None


def account(update, context):
    """
    Запись лицевого счёта пользователя. Лицевой счёт закрепляется за аккаунтом
    с именем пользователя из update.message.from_user
    :param update:
    :param context:
    :return:
    """
    try:
        with db.atomic():
            accounts = Agent.create(
                account_id=int(update.message.text)
            )
            user = User.get(User.username == update.message.from_user['username'])
            user.agent = accounts
            accounts.save()
            user.save()
            context.user_data["status"] = None
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Ваш серийный номер успешно прикреплён к аккаунту.")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Извините! Произошла ошибка, при попытке сохранения лицевого счёта." +
                                      "Повторите попытку позже.")
        context.user_data["status"] = None
