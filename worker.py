from sqlalchemy.orm import sessionmaker
from models import engine, Post
from tbot import TBot

from datetime import datetime #import pytz
import time
from pprint import pprint

## Constants ##
TOKEN = '827940689:AAFH0jE2qa6wvid-3my020PSv1sRO_F5bDM'
CHAT_ID = -364030033
DELAY = 20
##

Session = sessionmaker(bind=engine)
session = Session()

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
        post = Post(
            name=name,
            date=datetime.fromtimestamp(date), #pytz.timezone('singapore')
            message=text,
            photo=photo_path,
            caption=caption
        )
        session.add(post)
        session.commit()