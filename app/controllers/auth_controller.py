import re

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.models.user import User

auth_bp = Blueprint("auth", __name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_register(form):
    errors = []

    first_name = form.get("first_name", "").strip()
    last_name = form.get("last_name", "").strip()
    email = form.get("email", "").strip().lower()
    password = form.get("password", "")
    confirm = form.get("confirm_password", "")

    if len(first_name) < 2:
        errors.append("El nombre debe tener mínimo 2 caracteres.")

    if len(last_name) < 2:
        errors.append("El apellido debe tener mínimo 2 caracteres.")

    if not EMAIL_PATTERN.match(email):
        errors.append("Ingresa un correo válido.")

    if len(password) < 8:
        errors.append("La contraseña debe tener mínimo 8 caracteres.")

    if password != confirm:
        errors.append("Las contraseñas no coinciden.")

    if User.find_by_email(email):
        errors.append("Ese correo ya está registrado.")

    return errors


@auth_bp.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("books.index"))

    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("books.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.find_by_email(email)

        if user and User.check_password(password, user.password):
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.first_name

            flash(f"Bienvenido/a, {user.first_name}.", "success")
            return redirect(url_for("books.index"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("books.index"))

    if request.method == "POST":
        errors = validate_register(request.form)

        if errors:
            for error in errors:
                flash(error, "danger")

            return render_template("auth/register.html"), 400

        user_id = User.create(
            request.form["first_name"].strip(),
            request.form["last_name"].strip(),
            request.form["email"].strip().lower(),
            request.form["password"]
        )

        session.clear()
        session["user_id"] = user_id
        session["user_name"] = request.form["first_name"].strip()

        flash("Cuenta creada correctamente.", "success")
        return redirect(url_for("books.index"))

    return render_template("auth/register.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))
