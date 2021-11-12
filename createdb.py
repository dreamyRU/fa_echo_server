import sqlite3

connection = sqlite3.connect('./storage.db')
cursor = connection.cursor()

query = '''
CREATE TABLE users (
    ip varchar(50),
    name varchar(50),
    password varchar(50)
);'''

cursor.execute(query)