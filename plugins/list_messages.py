from sqlitedict import SqliteDict

def get_from_db():
    db = SqliteDict("db/db.sqlite")
    messages = db['messages']
    db.close()
    return messages

def format_messages(messages):
    for item in messages:
        print(item, ' -> ', messages[item])