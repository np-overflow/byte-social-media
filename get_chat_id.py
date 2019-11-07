from tbot import TBot

TOKEN = '827940689:AAFH0jE2qa6wvid-3my020PSv1sRO_F5bDM'
tbot = TBot(TOKEN)

for update in tbot.get_updates():
    message = update.get('message')
    if not message: continue
    chat_id = message['chat']['id']
    print(chat_id)