from tbot import TBot
from pprint import pprint

TOKEN = '827940689:AAFH0jE2qa6wvid-3my020PSv1sRO_F5bDM'
tbot = TBot(TOKEN)

x = lambda: tbot.get_updates()