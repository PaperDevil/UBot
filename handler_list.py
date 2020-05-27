from telegram.ext import CommandHandler

from Application.controls.commands import send_help

BASIC_COMMANDS = [
    CommandHandler('start', send_help),
    CommandHandler('help', send_help)
]