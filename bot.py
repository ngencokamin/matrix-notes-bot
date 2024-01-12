from dotenv import dotenv_values
import simplematrixbotlib as botlib
from sqlitedict import SqliteDict
from plugins.add_new import add_to_db
from plugins.list_messages import get_from_db, format_messages
from plugins.refresh_list import refresh
from plugins.run_command import get_by_command

db = SqliteDict("db/db.sqlite")

config = dotenv_values(".env")


homeserver = config['HOMESERVER']
user = config['USER']
password = config['PASS']
"""
Example Usage:

random_user
      *emoji verification or one-sided verification

random_user
      !echo something

echo_bot
      something
"""


config = botlib.Config()
# config.encryption_enabled = True  # Automatically enabled by installing encryption support
config.emoji_verify = True
config.ignore_unverified_devices = True

creds = botlib.Creds(homeserver, user, password)
bot = botlib.Bot(creds, config)
PREFIX = '!'

commands = refresh()

@bot.listener.on_message_event
async def add(room, message):
      match = botlib.MessageMatch(room, message, bot, PREFIX)
      if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("add")\
            and (room.power_levels.get_user_level(message.sender) == 100 or message.sender == '@matchstick:beeper.com'):
      
            args = match.args()
      
            add_msg = add_to_db(args)
      
            global commands
            commands = refresh()
            await bot.api.send_markdown_message(room.room_id, add_msg)
      elif match.prefix() and match.command("add") and (room.power_levels.get_user_level(message.sender) != 100 or message.sender != '@matchstick:beeper.com'):
            await bot.api.send_text_message(room.room_id, 'Error! You do not have permission to add new messages!')
          

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("echo"):
                  
        print(room.power_levels.get_user_level(message.sender))
        await bot.api.send_text_message(room.room_id, " ".join(arg for arg in match.args()))

@bot.listener.on_message_event
async def list(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("list"):
                  
      commands = get_from_db()
      format_messages(commands)
      await bot.api.send_markdown_message(room.room_id, "\n".join('- ' + str(item) for item in commands))

@bot.listener.on_message_event
async def send_command(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command() in commands:
            
      message_text = get_by_command(match.command())
      await bot.api.send_markdown_message(room.room_id, message_text)

bot.run()
