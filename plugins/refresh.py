from sqlitedict import SqliteDict

def refresh():
    db = SqliteDict("db/db.sqlite")
    rooms = {}
    for room in db:
        rooms[room] = db[room]
    db.close()
    return rooms

def verify_and_add_rooms(room_list):
    db = SqliteDict("db/db.sqlite")
    
    # Get rooms in DB
    db_rooms = [room for room in db]
    # Get rooms from bot api
    joined_rooms = [room for room in room_list]
    
    for room in joined_rooms:
        if not room in db_rooms:
            db[room] = {'messages': {}, 'allowed_users': []}
    
    db.commit()
    db.close()

def add_invited_room(room_id):
    db = SqliteDict("db/db.sqlite")
    rooms = db
    rooms[room_id] = {'messages': {}, 'allowed_users': []}
    db = rooms
    db.commit()
    db.close()
