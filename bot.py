from dotenv import dotenv_values
import simplematrixbotlib as botlib
from sqlitedict import SqliteDict
from plugins.add_new import add_to_db
from plugins.refresh import refresh, verify_and_add_rooms, add_invited_room
from plugins.run_command import get_by_command
from plugins.perms import has_permissions, add_user, remove_user
import time
import nio

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

rooms = refresh()
commands = ['add', 'remove', 'edit', 'add_user', 'echo', 'list', 'sync']

@bot.listener.on_message_event
async def add(room, message):
      match = botlib.MessageMatch(room, message, bot, PREFIX)
      
      global rooms
      if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("add")\
            and has_permissions(room, message, rooms):
            # and (room.power_levels.get_user_level(message.sender) == 100 or message.sender == '@matchstick:beeper.com'):
      
            args = match.args()
            body = message.body
      
            add_msg = add_to_db(body, room.room_id)
      
            rooms = refresh()
            await bot.api.send_markdown_message(room.room_id, add_msg)
      elif match.prefix()\
            and match.command("add"):
            await bot.api.send_text_message(room.room_id, 'Error! You do not have permission to add new messages!')
          

@bot.listener.on_message_event
async def list(room, message):
      match = botlib.MessageMatch(room, message, bot, PREFIX)
      if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("list"):
            
            if not rooms or not rooms[room.room_id]:
                  await bot.api.send_text_message(room.room_id, 'Error! No saved messages found!')
            else:
                  await bot.api.send_markdown_message(room.room_id, "\n".join('- ' + str(item) for item in rooms[room.room_id]['messages']))

@bot.listener.on_message_event
async def send_command(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    

    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command() not in commands\
            and rooms\
            and rooms[room.room_id]\
            and match.command() in rooms[room.room_id]['messages']:
            
            message_text = get_by_command(match.command(), room.room_id)
            await bot.api.send_markdown_message(room.room_id, message_text)


@bot.listener.on_message_event
async def sync_db(room, message):
      match = botlib.MessageMatch(room, message, bot, PREFIX)

      if match.is_not_from_this_bot()\
      and match.prefix()\
      and match.command("sync")\
      and message.sender == '@matchstick:beeper.com':
            joined_rooms = bot.api.async_client.rooms
            verify_and_add_rooms(joined_rooms)
            global rooms
            rooms = refresh()
            
@bot.listener.on_message_event
async def add_allowed_user(room, message):
      match = botlib.MessageMatch(room, message, bot, PREFIX)
      
      
      global rooms
      if match.is_not_from_this_bot()\
      and match.prefix()\
      and match.command("add_user")\
      and has_permissions(room, message, rooms):
            response = add_user(message.formatted_body, room.room_id)
            rooms = refresh()
            await bot.api.send_text_message(room.room_id, response)
      elif match.is_not_from_this_bot()\
      and match.prefix()\
      and match.command("add_user"): 
            await bot.api.send_text_message(room.room_id, 'Error! You do not have permission to add users to the allowlist!')
            
@bot.listener.on_message_event
async def remove_allowed_user(room, message):
      match = botlib.MessageMatch(room, message, bot, PREFIX)
      
      global rooms
      if match.is_not_from_this_bot()\
      and match.prefix()\
      and match.command("remove_user")\
      and has_permissions(room, message, rooms):
            response = remove_user(message.formatted_body, room.room_id)
            rooms = refresh()
            await bot.api.send_text_message(room.room_id, response)
      elif match.is_not_from_this_bot()\
      and match.prefix()\
      and match.command("remove_user"): 
            await bot.api.send_text_message(room.room_id, 'Error! You do not have permission to remove users from the allowlist!')
            
@bot.listener.on_custom_event(nio.InviteEvent)
async def test_event(room, event):
      if event.state_key == bot.async_client.user_id\
            and event.content['membership'] == 'invite'\
            and not event.prev_content:
                  add_invited_room(room.room_id)
                  global rooms
                  rooms = refresh()
      

bot.run()
