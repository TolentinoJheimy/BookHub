from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for("auth.login"))

        return view_function(*args, **kwargs)

    return wrapper
