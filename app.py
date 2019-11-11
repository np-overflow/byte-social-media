from flask import Flask, request
import requests
from tbot import TBot
from pprint import pprint
app = Flask(__name__)

TOKEN = '827940689:AAFH0jE2qa6wvid-3my020PSv1sRO_F5bDM'
HOST = '94.237.74.114'
URL = f'/telegram/{TOKEN}'
WEBHOOK_URL = f'{HOST}/{URL}'

bot = TBot(TOKEN)

@app.route(URL, methods=['POST'])
def telegram():
    pprint(request.json)
    return ''

if __name__ == "__main__":
    bot.set_webhook(WEBHOOK_URL)
    app.run(host=URL, port=80, debug=True)