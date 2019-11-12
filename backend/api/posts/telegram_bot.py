import uuid
import os
import urllib
import requests


def _create_url(token, url_path):
    return f'https://api.telegram.org/bot{token}/{url_path}'


def _create_file_url(token, url_path):
    return f'https://api.telegram.org/file/bot{token}/{url_path}'


def _bot_request(token, url_path, **params):
    url = _create_url(token, url_path)
    response = requests.get(url, **params)
    return response.json()['result']


def _create_filename(file_ext):
    return f'{uuid.uuid4().hex}{file_ext}'


def download_image(token, file_id, download_location):
    # Get the file url
    params = {"file_id": file_id}
    response = _bot_request(token, 'getFile', json=params)

    # Download
    file_path = file_path = response['file_path']

    file_ext = os.path.splitext(file_path)[1]
    filename = _create_filename(file_ext)
    file_url = _create_file_url(token, file_path)

    urllib.request.urlretrieve(
        file_url, os.path.join(download_location, filename))

    return filename


def send_message(token, chat_id, text):
    params = {'chat_id': chat_id, 'text': text}
    response = _bot_request(token, 'sendMessage', json=params)
    return response
