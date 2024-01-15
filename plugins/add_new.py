from sqlitedict import SqliteDict

def parse_opts(arr):
    
    message = []
    
    command = "".join(arr[arr.index('--command')+1:arr.index('--message')])
    message = " ".join(arr[arr.index('--message')+1:len(arr)])
    return [command, message]

def add_to_db(args, room_id):
    required = ["--command", "--message"]
    if not all(arg in args for arg in required):
        return 'Error! You must specify command name and message contents<br>**example usage:** `!add --command [command name] --message [message contents]`'
    opts = parse_opts(args)
    db = SqliteDict("db/db.sqlite", autocommit=True)
    if not db or not db[room_id]:
        db[room_id]['messages'] = {opts[0]: opts[1]}
        db.commit()
    else:
        room = db[room_id]
        room['messages'][opts[0]] = opts[1]
        db[room_id] = room

    
    db.close()
    return f'Added command `{opts[0]}`!'
