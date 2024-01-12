from sqlitedict import SqliteDict

def get_by_command(command):
    db = SqliteDict("db/db.sqlite")
    messages = db['messages']
    return messages[command]