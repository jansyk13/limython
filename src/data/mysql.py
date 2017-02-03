import MySQLdb

# DB utils module


def get_connection():
    db = MySQLdb.connect(host="localhost", user="root",
                         passwd="password", db="mlrl")
    return db


def get_cursor(db=None):
    _db = db
    if (_db is None):
        _db = get_connection()

    return _db.cursor()
