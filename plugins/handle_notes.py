from sqlitedict import SqliteDict

def parse_opts(message_body):
    
    start_command = message_body.find('--command ') + 10
    end_command = message_body.find(' --message')
    command = message_body[start_command:end_command]
    
    start_message = message_body.find('--message ') + 10
    message = message_body[start_message:]
    
    return [command, message]

def add_to_db(body, room_id):
    required = ["--command", "--message"]
    if not all(arg in body for arg in required):
        return 'Error! You must specify command name and message contents<br>**example usage:** `!add --command [command name] --message [message contents]`'
    opts = parse_opts(body)
    db = SqliteDict("db/db.sqlite")
    if not db or not db[room_id]:
        db[room_id]['messages'] = {opts[0]: opts[1]}
    else:
        room = db[room_id]
        room['messages'][opts[0]] = opts[1]
        db[room_id] = room

    db.commit()
    db.close()
    return f'Added note `{opts[0]}`!'

def remove_from_db(arg, room_id):
    db = SqliteDict("db/db.sqlite")
    room = db[room_id]
    del room['messages'][arg]
    db[room_id] = room
    db.commit()
    db.close()
    return f'Removed note `{arg}`'