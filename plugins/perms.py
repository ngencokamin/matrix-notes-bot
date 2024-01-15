from sqlitedict import SqliteDict

def has_permissions(current_room, message, rooms):
    power_level = current_room.power_levels.get_user_level(message.sender)
    allowed_users = rooms[current_room.room_id]['allowed_users']
    is_allowed_user = False
    formatted_sender = message.sender[1:]
    
    if not len(allowed_users) == 0:
        for user in allowed_users:
            if user == formatted_sender:
                is_allowed_user = True
    if power_level == 100 or is_allowed_user:
        return True
    else:
        return False
    

def parse_user(message_body):
    if not message_body:
        return False
    start = 'https://matrix.to/#/'
    end = '">'
    
    idx1 = message_body.index(start)
    idx2 = message_body.index(end)
    
    user = message_body[idx1 + len(start) + 1: idx2]
    
    return user


def add_user(message_body, room_id):
    parsed_user = parse_user(message_body)
    if not parsed_user:
        return 'Error! Please tag a valid user to add!'
    db = SqliteDict("db/db.sqlite")
    if parsed_user in db[room_id]['allowed_users']:
        db.close()
        return f'User @{parsed_user} is already in allowlist!'
    else:
        room = db[room_id]
        room['allowed_users'].append(parsed_user)
        db[room_id] = room
        db.commit()
        db.close()
        return f'Added user @{parsed_user} to allowlist'
    
def remove_user(message_body, room_id):
    parsed_user = parse_user(message_body)
    if not parsed_user:
        return 'Error! Please tag a valid user to remove from allowlist!'
    db = SqliteDict("db/db.sqlite")
    if parsed_user not in db[room_id]['allowed_users']:
        db.close()
        return f'User @{parsed_user} is not currently in allowlist!'
    else:
        room = db[room_id]
        room['allowed_users'].remove(parsed_user)
        db[room_id] = room
        db.commit()
        db.close()
        return f'Removed user @{parsed_user} from allowlist'