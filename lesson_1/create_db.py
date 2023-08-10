import sqlite3

with sqlite3.connect('db.sqlite') as db:
    cur = db.cursor()

    with open('create_db.sql', 'r') as file:
        script = file.read()

    cur.executescript(script)
