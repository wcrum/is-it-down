from sqlmodel import create_engine

from flask import current_app as app

engine = create_engine(app.config["DATABASE_URI"])
