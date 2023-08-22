import sqlite3

connection = sqlite3.connect('database.db')


with open('db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO people (person) VALUES ('Tom')")
cur.execute("INSERT INTO people (person) VALUES ('Peter')")
cur.execute("INSERT INTO people (person) VALUES ('Max')")
cur.execute("INSERT INTO people (person) VALUES ('Robert')")

connection.commit()
connection.close()