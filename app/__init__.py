from datetime import date
import os

from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "cambia-esta-clave"
    )

    @app.context_processor
    def inject_today():
        return {"today": date.today().isoformat()}

    from app.controllers.auth_controller import auth_bp
    from app.controllers.book_controller import book_bp
    from app.controllers.favorite_controller import favorite_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(favorite_bp)

    return app