from sqlitedict import SqliteDict

def get_from_db(room_id):
    db = SqliteDict("db/db.sqlite")
    if not db or not db[room_id]:
        return False
    messages = db[room_id]
    db.close()
    return messages
