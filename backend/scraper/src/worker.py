import models
from tbot import TBot

from datetime import datetime
import time
from pprint import pprint

## Constants ##
TOKEN = '827940689:AAFH0jE2qa6wvid-3my020PSv1sRO_F5bDM'
CHAT_ID = -364030033
DELAY = 20
##

tbot = TBot(TOKEN)
last_time = 0
while True:
    # Don't spam the server
    duration = time.time() - last_time
    print('Elapsed Time:', duration)
    time.sleep(max(0, DELAY - duration))
    last_time = time.time()

    updates = tbot.get_updates()
    for update in updates:
        # Check if is message
        message =   update.get('message')
        if message is None: continue
        # Check if from group
        chat_id =   message['chat']['id']
        if chat_id != CHAT_ID: continue

        # Parse Message
        msg_id =    message['message_id']
        name =      message['from']['first_name']
        date =      message['date']
        text =      message.get('text')
        caption =   message.get('caption')
        photo =     message.get('photo')
        photo_path = None
        if photo:
            file_id = photo[-1]['file_id']
            photo_path = tbot.download_file(file_id)

        # Skip invalid message
        if not any((text, photo)): continue
        
        # Add to DB
        media = models.create_media(
            kind=models.ContentType.Image,
            # TODO: Set the source to a URL to the file
            src=photo_path,
        )

        post = models.create_post(
            # TODO: Set the post ID, should be unique for all Telegram messages
            # and should be a string.
            # See models.int_id_to_str if you need a function to convert an
            # integer to a string.
            post_id=models.int_id_to_str(msg_id),
            platform=models.SocialPlatform.Telegram,
            date=datetime.fromtimestamp(date),
            author=name,
            caption=caption or message,
            media=media,
        )
