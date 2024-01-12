from sqlitedict import SqliteDict

def refresh():
    db = SqliteDict("db/db.sqlite")
    rooms = {}
    for room in db:
        rooms[room] = db[room]
    db.close()
    return rooms
