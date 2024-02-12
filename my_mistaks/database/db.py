import sqlite3

def connect_to_sqlite():
    try:
        conn = sqlite3.connect('mistakes.sqlite3')
        return conn
    except sqlite3.Error as e:
        print(e)
        return None
