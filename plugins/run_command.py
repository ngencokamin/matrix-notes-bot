from sqlitedict import SqliteDict

def get_by_command(command, room_id):
    db = SqliteDict("db/db.sqlite")
    messages = db[room_id]
    return messages[command]