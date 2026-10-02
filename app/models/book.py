from app.config import db


class Book:
    def __init__(
        self,
        id=None,
        title="",
        author="",
        genre="",
        publication_date=None,
        description="",
        user_id=None,
        owner_name=None,
        favorite_count=0,
        is_favorite=0,
        created_at=None
    ):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_date = publication_date
        self.description = description
        self.user_id = user_id
        self.owner_name = owner_name
        self.favorite_count = favorite_count or 0
        self.is_favorite = bool(is_favorite)
        self.created_at = created_at

    @classmethod
    def find_by_id(cls, book_id, user_id):
        query = """
            SELECT
                b.*,
                CONCAT(u.first_name, ' ', u.last_name) AS owner_name,
                COUNT(DISTINCT f.user_id) AS favorite_count,
                COALESCE(
                    MAX(CASE WHEN f.user_id = %s THEN 1 ELSE 0 END),
                    0
                ) AS is_favorite
            FROM books b
            INNER JOIN users u ON u.id = b.user_id
            LEFT JOIN favorites f ON f.book_id = b.id
            WHERE b.id = %s
            GROUP BY b.id
            LIMIT 1
        """
        rows = db.query_db(query, (user_id, book_id))
        return cls(**rows[0]) if rows else None

    @classmethod
    def create(
        cls,
        title,
        author,
        genre,
        publication_date,
        description,
        user_id
    ):
        query = """
            INSERT INTO books
                (title, author, genre, publication_date, description, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.query_db(
            query,
            (
                title,
                author,
                genre,
                publication_date,
                description,
                user_id
            )
        )

    @classmethod
    def update(
        cls,
        book_id,
        title,
        author,
        genre,
        publication_date,
        description,
        user_id
    ):
        query = """
            UPDATE books
            SET title = %s,
                author = %s,
                genre = %s,
                publication_date = %s,
                description = %s
            WHERE id = %s AND user_id = %s
        """
        return db.query_db(
            query,
            (
                title,
                author,
                genre,
                publication_date,
                description,
                book_id,
                user_id
            )
        )

    @classmethod
    def delete(cls, book_id, user_id):
        query = """
            DELETE FROM books
            WHERE id = %s AND user_id = %s
        """
        return db.query_db(query, (book_id, user_id))

    @classmethod
    def community_books(cls, user_id):
        query = """
            SELECT
                b.*,
                CONCAT(u.first_name, ' ', u.last_name) AS owner_name,
                COUNT(DISTINCT f.user_id) AS favorite_count,
                COALESCE(
                    MAX(CASE WHEN f.user_id = %s THEN 1 ELSE 0 END),
                    0
                ) AS is_favorite
            FROM books b
            INNER JOIN users u ON u.id = b.user_id
            LEFT JOIN favorites f ON f.book_id = b.id
            GROUP BY b.id
            ORDER BY b.created_at DESC
        """
        rows = db.query_db(query, (user_id,))
        return [cls(**row) for row in rows]
