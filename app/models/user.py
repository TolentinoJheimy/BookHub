import bcrypt

from app.config import db


class User:
    def __init__(
        self,
        id=None,
        first_name="",
        last_name="",
        email="",
        password="",
        created_at=None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = created_at

    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    @classmethod
    def find_by_email(cls, email):
        query = """
            SELECT id, first_name, last_name, email, password, created_at
            FROM users
            WHERE email = %s
            LIMIT 1
        """
        rows = db.query_db(query, (email,))
        return cls(**rows[0]) if rows else None

    @classmethod
    def create(cls, first_name, last_name, email, password):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%s, %s, %s, %s)
        """
        return db.query_db(
            query,
            (
                first_name,
                last_name,
                email,
                cls.hash_password(password)
            )
        )

    @classmethod
    def favorite_users_for_book(cls, book_id):
        query = """
            SELECT u.id, u.first_name, u.last_name, u.email
            FROM users u
            INNER JOIN favorites f ON f.user_id = u.id
            WHERE f.book_id = %s
            ORDER BY u.first_name, u.last_name
        """
        return db.query_db(query, (book_id,))
