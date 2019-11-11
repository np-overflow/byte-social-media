from flask import Flask, request
import requests
from tbot import TBot
from pprint import pprint
app = Flask(__name__)

TOKEN = '827940689:AAFH0jE2qa6wvid-3my020PSv1sRO_F5bDM'
HOST = '94.237.74.114'
PORT = 443
URL = f'/telegram/{TOKEN}'
WEBHOOK_URL = f'https://{HOST}{URL}'
PUBLIC_CERT_PATH = 'public.pem'

bot = TBot(TOKEN)

@app.route('/')
def index():
    return 'hello'

@app.route(URL, methods=['POST'])
def telegram():
    pprint(request.json)
    return ''

if __name__ == "__main__":
    bot.set_webhook(WEBHOOK_URL)
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=('public.pem', 'private.key'))