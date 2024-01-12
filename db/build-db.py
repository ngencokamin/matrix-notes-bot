from sqlitedict import SqliteDict
db = SqliteDict("db/db.sqlite")
db['messages'] = {}

db.commit()

db.close()