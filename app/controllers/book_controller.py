from datetime import date

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.models.book import Book
from app.models.user import User
from app.utils.auth import login_required

book_bp = Blueprint("books", __name__, url_prefix="/libros")

GENRES = [
    "Novela",
    "Ciencia Ficción",
    "Fantasía",
    "Romance",
    "Misterio",
    "Terror",
    "Historia",
    "Desarrollo Personal",
    "Fábula",
    "Otro",
]


def validate_book(form):
    errors = []

    title = form.get("title", "").strip()
    author = form.get("author", "").strip()
    genre = form.get("genre", "").strip()
    publication_date = form.get("publication_date", "").strip()
    description = form.get("description", "").strip()

    if len(title) < 2:
        errors.append("El título debe tener mínimo 2 caracteres.")

    if not author:
        errors.append("El autor es obligatorio.")

    if genre not in GENRES:
        errors.append("Debes seleccionar un género válido.")

    if not publication_date:
        errors.append("La fecha de publicación es obligatoria.")
    else:
        try:
            selected_date = date.fromisoformat(publication_date)

            if selected_date > date.today():
                errors.append("La fecha no puede ser futura.")
        except ValueError:
            errors.append("La fecha no es válida.")

    if len(description) < 10:
        errors.append("La descripción debe tener mínimo 10 caracteres.")

    return errors


@book_bp.route("")
@login_required
def index():
    user_id = session["user_id"]

    my_books = [
        book for book in Book.community_books(user_id)
        if book.user_id == user_id
    ]

    community_books = Book.community_books(user_id)

    return render_template(
        "books/index.html",
        my_books=my_books,
        community_books=community_books
    )


@book_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def new_book():
    if request.method == "POST":
        errors = validate_book(request.form)

        if errors:
            for error in errors:
                flash(error, "danger")

            return render_template(
                "books/form.html",
                book=request.form,
                genres=GENRES,
                form_title="Agregar Nuevo Libro",
                submit_text="Guardar"
            ), 400

        Book.create(
            request.form["title"].strip(),
            request.form["author"].strip(),
            request.form["genre"].strip(),
            request.form["publication_date"],
            request.form["description"].strip(),
            session["user_id"]
        )

        flash("Libro creado correctamente.", "success")
        return redirect(url_for("books.index"))

    return render_template(
        "books/form.html",
        book=None,
        genres=GENRES,
        form_title="Agregar Nuevo Libro",
        submit_text="Guardar"
    )


@book_bp.route("/<int:book_id>")
@login_required
def detail(book_id):
    book = Book.find_by_id(book_id, session["user_id"])

    if not book:
        flash("El libro no existe.", "danger")
        return redirect(url_for("books.index"))

    favorite_users = User.favorite_users_for_book(book_id)

    return render_template(
        "books/detail.html",
        book=book,
        favorite_users=favorite_users
    )


@book_bp.route("/editar/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit(book_id):
    user_id = session["user_id"]
    book = Book.find_by_id(book_id, user_id)

    if not book:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for("books.index"))

    if book.user_id != user_id:
        flash("No puedes editar un libro que no es tuyo.", "danger")
        return redirect(url_for("books.index"))

    if request.method == "POST":
        errors = validate_book(request.form)

        if errors:
            for error in errors:
                flash(error, "danger")

            return render_template(
                "books/form.html",
                book=request.form,
                genres=GENRES,
                form_title="Editar Libro",
                submit_text="Actualizar"
            ), 400

        Book.update(
            book_id,
            request.form["title"].strip(),
            request.form["author"].strip(),
            request.form["genre"].strip(),
            request.form["publication_date"],
            request.form["description"].strip(),
            user_id
        )

        flash("Libro actualizado correctamente.", "success")
        return redirect(url_for("books.index"))

    return render_template(
        "books/form.html",
        book=book,
        genres=GENRES,
        form_title="Editar Libro",
        submit_text="Actualizar"
    )


@book_bp.route("/borrar/<int:book_id>", methods=["POST"])
@login_required
def delete(book_id):
    user_id = session["user_id"]
    book = Book.find_by_id(book_id, user_id)

    if not book:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for("books.index"))

    if book.user_id != user_id:
        flash("Solo puedes borrar tus propios libros.", "danger")
        return redirect(url_for("books.index"))

    Book.delete(book_id, user_id)

    flash("Libro eliminado correctamente.", "success")
    return redirect(url_for("books.index"))
