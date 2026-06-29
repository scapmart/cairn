import sqlite3

class Database:

    def __init__(self, path="cairn.db"):
        self.conn = sqlite3.connect(path)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()