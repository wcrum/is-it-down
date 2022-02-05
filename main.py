import os
from flask import Flask

import os
import requests
from app import config
from app.routes import default
from app.routes import debug
from app.routes import auth
from app.routes import admin
from app.routes import profile
from app.routes import server
from app.pages import create_pages
from sqlmodel import SQLModel
from sqlmodel import create_engine

from app.models.user import Log, User

APP_SETTINGS = os.getenv("APP_SETTINGS", "Testing")


def drop_database(config):
    import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import inspect
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    engine = create_engine(config["DATABASE_URI"])
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(engine, checkfirst=False)


def create_app():
    app = Flask(__name__, template_folder="app/templates/", static_folder="app/static/")
    app.count_requests = 0

    app.config.from_object(f"app.config.{APP_SETTINGS}")
    app.secret_key = os.urandom(256)
    app.url_map.strict_slashes = False

    app.register_blueprint(default.bp)
    app.register_blueprint(debug.bp, url_prefix="/debug")
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(admin.bp, url_prefix="/admin")
    app.register_blueprint(profile.bp, url_prefix="/user")
    app.register_blueprint(server.bp, url_prefix="/server")
    app.register_error_handler(Exception, default.handle_exception)

    return app


app = create_app()
app.pages = create_pages()
with app.app_context():
    from app.database import engine

    app.engine = engine

if os.getenv("DROP_DATABASE", False):
    drop_database(app.config)

SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(host=app.config.get("HOST"), port=app.config.get("PORT"))
