"""Flask entrypoint for Smart Campus Navigation System."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from models import init_db
from routes import api

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
ASSETS_DIR = BASE_DIR.parent / "static"


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
    CORS(app)

    init_db()
    app.register_blueprint(api)

    @app.get("/")
    def serve_frontend():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/assets/<path:filename>")
    def serve_assets(filename: str):
        """Serve static map/image assets from the top-level static directory."""
        return send_from_directory(ASSETS_DIR, filename)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)
