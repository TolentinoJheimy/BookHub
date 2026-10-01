from flask import Blueprint, flash, redirect, render_template, session, url_for

from app.models.book import Book
from app.models.favorite import Favorite
from app.utils.auth import login_required

favorite_bp = Blueprint("favorites", __name__)


@favorite_bp.route("/favorito/<int:book_id>/toggle", methods=["POST"])
@login_required
def toggle(book_id):
    user_id = session["user_id"]
    book = Book.find_by_id(book_id, user_id)

    if not book:
        flash("El libro no existe.", "danger")
        return redirect(url_for("books.index"))

    if book.is_favorite:
        Favorite.remove(user_id, book_id)
        flash("Libro quitado de favoritos.", "info")
    else:
        Favorite.add(user_id, book_id)
        flash("Libro agregado a favoritos.", "success")

    return redirect(url_for("books.detail", book_id=book_id))


@favorite_bp.route("/favoritos")
@login_required
def index():
    books = Favorite.for_user(session["user_id"])
    return render_template("favorites/index.html", books=books)
