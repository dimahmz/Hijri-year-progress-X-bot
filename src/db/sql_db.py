import sqlite3


class sqlDB:
    connection: sqlite3.Connection = None

    def __init__(self, dbname: str):
        self.connection = sqlite3.connect(dbname)

    def createConnection(self, dbname: str) -> sqlite3.Connection:
        # @TODO wha if the database doesn't exist
        if (self.connection):
            return self.connection
        connection = sqlite3.connect(dbname)
        return connection

    def closeConnection(self):
        # what if the connection is incorrect
        if (self.connection):
            self.connection.close()

    def createTable(self, query: str) -> sqlite3.Cursor:
        # what if the connection is invalid
        if (self.connection == None):
            raise ("must create a connection before creating a table")
        cursor = self.connection.cursor()
        return cursor.execute(f"{query}")
