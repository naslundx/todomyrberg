import os
from flask import Flask
from flask_cors import CORS


from typing import Any


def create_app() -> Flask:
    flask_app = Flask(__name__, static_folder="../frontend/dist/", static_url_path="/")
    CORS(flask_app)

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:password@localhost:5432/todomyrberg"
    )
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from src.models import db

    db.init_app(flask_app)

    from src.routes import api

    flask_app.register_blueprint(api, url_prefix="/api")

    @flask_app.route("/", defaults={"path": ""})
    @flask_app.route("/<path:path>")
    def catch_all(path: str) -> Any:
        if path != "" and os.path.exists(
            os.path.join(flask_app.static_folder or "", path)
        ):
            return flask_app.send_static_file(path)
        return flask_app.send_static_file("index.html")

    return flask_app


app = create_app()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", threaded=True, port=PORT)
