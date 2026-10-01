import os

import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()


class MySQLConnection:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "bookhub")

    def connect(self):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        connection = self.connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, data or ())

                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()

                if query.strip().lower().startswith("insert"):
                    return cursor.lastrowid

                return True
        finally:
            connection.close()

    def execute(self, query, data=None):
        connection = self.connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, data or ())
                return True
        finally:
            connection.close()


db = MySQLConnection()


def init_app():
    return db
