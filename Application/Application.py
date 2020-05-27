from telegram.ext import Updater, CommandHandler

class BotApplication(Updater):
    def __init__(self, token, request_args, handlers):
        super().__init__(token, request_kwargs=request_args, use_context=True)

        for handler in handlers:
            self.register_command(handler)

    def register_command(self, handler):
        self.dispatcher.add_handler(handler)

    def start(self):
        self.start_polling()

