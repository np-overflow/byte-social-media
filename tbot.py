import requests
import os
import urllib.request
import uuid

IMAGE_FOLDER = 'images'

class TBot:
    def __init__(self, token):
        self.token = token
        self.url = f'https://api.telegram.org/bot{token}/'
        self.file_url = f'https://api.telegram.org/file/bot{token}/'
        self.last_id = None

        if not os.path.isdir(IMAGE_FOLDER):
            os.mkdir(IMAGE_FOLDER)

    def request(self, method, *args, **kwargs):
        response = requests.get(self.url + method, *args, **kwargs)
        return response.json().get('result')
    
    def get_updates(self):
        params = {'offset': self.last_id}
        response = self.request('getUpdates', json=params)
        if response: self.last_id = response[-1]['update_id'] + 1
        return response

    def download_file(self, file_id):
        # Get File Path
        params = {'file_id': file_id}
        response = self.request('getFile', json=params)
        file_path = response['file_path']
        file_ext = os.path.splitext(file_path)[1]
        # Download
        file_name = f'{uuid.uuid4().hex}{file_ext}'
        urllib.request.urlretrieve(self.file_url + file_path, os.path.join(IMAGE_FOLDER, file_name))
        return file_name

    def set_webhook(self, webhook_url):
        params = {'url': webhook_url}
        response = self.request('setWebhook', files=params)
        return response

    # def set_webhook(self, webhook_url, cert_path):
    #     params = {'url': webhook_url, 'certificate': cert_path}
    #     response = self.request('setWebhook', json=params)
    #     return response