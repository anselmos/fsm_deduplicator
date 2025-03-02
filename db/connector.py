import psycopg2

from constants import DB_URL

class DBConnector:

    def __init__(self):
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

    @staticmethod
    def get_connection():
        return psycopg2.connect(DB_URL)

    def get_cursor(self):
        return self.get_connection().cursor()

    def close(self):
        self.connection.close()

    def execute(self, query):
        self.cursor.execute(query)