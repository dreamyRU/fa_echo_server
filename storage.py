from hashlib import sha256
import sqlite3


class Database:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def createUser(self, IP, name, password):
        hash_password = sha256(password.encode('utf-8')).hexdigest()
        self.cursor.execute("INSERT INTO users VALUES('{}', '{}', '{}')".format(IP, name, hash_password))
        self.connection.commit()


    def login(self, name, password):
        hash_password = sha256(password.encode('utf-8')).hexdigest()
        data = self.cursor.execute("SELECT * FROM users WHERE name='{}'".format(name)).fetchone()
        return data[2] == hash_password
        

    def checkIP(self, IP):
        name = self.cursor.execute("SELECT name FROM users WHERE ip='{}'".format(IP)).fetchone()
        return name[0] if name else None
        

