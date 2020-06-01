from .Application import BotApplication


def get_app(config: dict, handlers: list = []):
    """
    :param config: dict
    :param handlers: list
    :return app: Updater
    """
    app = BotApplication(
        token=config["TOKEN"],
        request_args=config["REQUEST_KWARGS"],
        handlers=handlers
    )

    return app
