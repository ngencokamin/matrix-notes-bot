from sqlitedict import SqliteDict
db = SqliteDict("db/db.sqlite")

db.commit()

db.close()