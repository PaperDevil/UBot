from telegram.ext import CommandHandler, MessageHandler, Filters

from Application.controls import commands

DEBUG_COMMANDS = [
CommandHandler('status', commands.status),
]

NLP_TEST_COMMANDS = [
    MessageHandler(Filters.text & (~Filters.command), commands.QAnswer)
]

WORKING_COMMANDS = [
    CommandHandler('indicates', commands.get_indicates),
    CommandHandler('register', commands.register_user),
    CommandHandler('account', commands.get_personal_account),
    CommandHandler('stop', commands.stop)
]

BASIC_COMMANDS = [
    CommandHandler('start', commands.send_help),
    CommandHandler('help', commands.send_help)
]
BASIC_COMMANDS += NLP_TEST_COMMANDS
BASIC_COMMANDS += WORKING_COMMANDS
BASIC_COMMANDS += DEBUG_COMMANDS
