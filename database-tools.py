import sys
import os
import click
from app import config
from sqlmodel import Session
from sqlmodel import create_engine
from app.models.server import Server
from sqlmodel import select

API_ENVIRONMENT = os.environ.get("API_ENVIRONMENT", "Testing")
settings = getattr(sys.modules[__name__].config, API_ENVIRONMENT)

engine = create_engine(settings.DATABASE_URI)


@click.group()
@click.pass_context
def main():
    pass


@main.command(name="settings")
def get_settings():
    """
    Prints current API settings from $API_ENVIRONMENT.
    """
    click.echo(settings)


@main.group(name="import")
def import_group():
    pass

@import_group.command(name="catagories")
def import_catagories():
    """
    Commands for importing a database.
    """

    import yaml
    from app.models.server import Catagory, ServerCatagoryLink
    print("Looking for catagories.yml")

    with Session(engine) as session:
        with open("config.yml", "r") as stream:
            catagories = yaml.safe_load(stream)

            for name, data in catagories.get("catagories").items():
                print(data)
                _catagory = Catagory(
                    title = name,
                    meta_ref = name.lower().replace(" ", "-"),
                    color = f"#{data['color']}"
                )

                session.add(_catagory)
                session.commit()
                session.refresh(_catagory)

                _query = select(Server).where(Server.domain_name.like(data['match']))
                _result = session.exec(_query).all()
                for server in _result:
                    _link = ServerCatagoryLink(
                        server_id = server.id,
                        catagory_id = _catagory.id
                    )
                    session.add(_link)
                session.commit()

@import_group.command(name="csv")
def csv_file(file):
    """
    Commands for importing a database.
    """
    import csv

    with Session(engine) as session:
        with open(file, "r") as stream:
            csv_reader = csv.DictReader(stream)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1

                _server = Server(
                    domain_name=row["Domain Name"],
                    domain_type=row["Domain Type"],
                    agency=row["Agency"],
                    organization=row["Organization"],
                )
                session.add(_server)
        session.commit()


@import_group.command(name="file")
@click.argument("file")
def basic_file(file):
    with Session(engine) as session:
        with open(file, "r") as stream:
            stream = stream.readlines()
            servers = []
            for row in stream:
                servers.append(row.strip().lower())

            for row in list(set(servers)):
                session.add(Server(domain_name=row))

        session.commit()


@main.group()
def tables():
    """
    Commands for handling database tables.
    """
    pass


@tables.command()
def drop():
    """
    Forcefully remove all tables within the database.
    """
    import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import inspect
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    engine = create_engine(settings.DATABASE_URI)
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(engine, checkfirst=False)
    print("Dropped tables.")


@tables.command()
def create():
    """
    Creates all tables within the API.
    """
    from sqlmodel import SQLModel
    from app.models.user import User, Log
    from app.models.server import Server, ServerLog

    SQLModel.metadata.create_all(engine)
    print("Created tables.")


cli = click.CommandCollection(sources=[main])

if __name__ == "__main__":
    cli()
