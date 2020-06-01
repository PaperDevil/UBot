from Application import get_app
from handler_list import BASIC_COMMANDS

from Application.models.models import *

try:
    with db.atomic():
        db.create_tables([Agent, User, Indicate])
        print("Database succesfuled created.")
except:
    print("Database already exist.")

config = {
    'TOKEN': '1197366717:AAGk6U7qA2Bg1mGp25aBWqpFlsKNTe5CMtQ',
    'REQUEST_KWARGS': {
        'proxy_url': 'socks5://207.97.174.134:1080/'
    },
    'GOOGLE_SHEETS': {
        'token_json': 'credentials.json',
        'spreadsheet_id': ''
    }
}

if __name__ == '__main__':
    app = get_app(config, BASIC_COMMANDS)
    app.start()