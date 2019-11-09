### A. Pre-Setup
1. Create a Telegram Group
2. Create a Telegram Bot (Talk to botfather)
3. Retrieve the Bot ID (Talk to botfather)
4. Add Bot to Group

### B. Retrieve Group ID (get_chat_id.py)
1. Send a Message to Group
2. Replace with your bot token in get_chat_id.py
3. Run get_chat_id.py 
    > python get_chat_id.py
4. You should see chat id(s) from the messages that the bot has received.

### C. Run Worker (worker.py)
1. Replace your bot token in worker.py
2. Replace your chat id in worker.py
3. Run worker.py
    > python worker.py

Worker will read only from chat with the stated chat id.

### File Structure
1. ion.py - Testing Purposes
2. models.py - Database Models
3. tbot.py - Contains TBot Class to interface telegram
4. worker.py - The Worker
5. get_chat_id.py - Get chat id from messages received by bot.
