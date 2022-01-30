import os
import sys
import click
import sqlalchemy
import importlib

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

settings = os.getenv("APP_SETTINGS", "Testing")
engine = create_engine(config.DATABASE_URI)
meta = MetaData()
meta.reflect(bind=engine)

inspector = inspect(engine)

# This file is meant for production/development environments only
# This file is nessecary because the limitations of pythons ORM
# Changes to the schema will not reflect unless using a different


def drop_tables():
    """
    This will forcfully remove all tables within the database.
    """
    # This is intended to be used as a "reset" for the database
    # Changes with the ORM at creation will not create the tables
    # Check for $env:RESET_DATABASE and run this function if true
    meta.drop_all(engine, checkfirst=False)


def update():
    # This is intended to keep the data but update the tables
    pass
