from flask import Flask, request
import requests
from pprint import pprint
app = Flask(__name__)

TOKEN = '827940689:AAFH0jE2qa6wvid-3my020PSv1sRO_F5bDM'

@app.route('/telegram', method=['POST'])
def telegram():
    pprint(request.json)
    return ''

if __name__ == "__main__":
    