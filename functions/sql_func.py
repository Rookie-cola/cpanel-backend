import sqlite3


def execute(*args, **kwargs):
    conn = sqlite3.connect('db/Linux.db')
    cursor = conn.cursor()
    cursor.execute(*args, **kwargs)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def insert(*args, **kwargs):
    conn = sqlite3.connect('db/Linux.db')
    cursor = conn.cursor()
    cursor.execute(*args, **kwargs)
    result = cursor.lastrowid
    conn.commit()
    conn.close()
    return result

