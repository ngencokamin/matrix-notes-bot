from sqlitedict import SqliteDict

def refresh():
    db = SqliteDict("db/db.sqlite")
    commands = []
    for command in db['messages']:
        commands.append(command)
    db.close()
    return commands
