from app.config import db


class Favorite:
    @staticmethod
    def add(user_id, book_id):
        query = """
            INSERT IGNORE INTO favorites (user_id, book_id)
            VALUES (%s, %s)
        """
        return db.query_db(query, (user_id, book_id))

    @staticmethod
    def remove(user_id, book_id):
        query = """
            DELETE FROM favorites
            WHERE user_id = %s AND book_id = %s
        """
        return db.query_db(query, (user_id, book_id))

    @staticmethod
    def for_user(user_id):
        query = """
            SELECT
                b.*,
                CONCAT(u.first_name, ' ', u.last_name) AS owner_name,
                COUNT(DISTINCT f2.user_id) AS favorite_count,
                1 AS is_favorite
            FROM favorites f
            INNER JOIN books b ON b.id = f.book_id
            INNER JOIN users u ON u.id = b.user_id
            LEFT JOIN favorites f2 ON f2.book_id = b.id
            WHERE f.user_id = %s
            GROUP BY b.id
            ORDER BY f.created_at DESC
        """
        return db.query_db(query, (user_id,))
