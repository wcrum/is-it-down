import os
import sys
from threading import Thread, Lock
from queue import Queue
from app import config
from app.models.server import Server, ServerLog
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import select
from datetime import datetime
import requests

API_ENVIRONMENT = os.environ.get("API_ENVIRONMENT", "Testing")
settings = getattr(sys.modules[__name__].config, API_ENVIRONMENT)

engine = create_engine(settings.DATABASE_URI)


def main_thread():
    with Session(engine) as session:
        server_list = session.exec(select(Server)).all()
        for server in server_list:
            error = None
            try:
                r = requests.get(
                    "http://" + server.domain_name, stream=True, timeout=30
                )

            except requests.exceptions.Timeout:
                error = "TIME OUT"
            except requests.exceptions.ConnectionError:
                error = "DOWN"
            except Exception:
                error = "GENERAL ERROR"

            if error == None:
                try:
                    address = r.raw._connection.sock.getpeername()
                    address = address[0]
                except Exception:
                    address = None

                _log = ServerLog(
                    server_id=server.id,
                    datetime=datetime.now(),
                    response_code=r.status_code,
                    response_time=r.elapsed.total_seconds() * 100,
                    ipaddress=address,
                    url=server.domain_name,
                )
                server.status = "UP"
                server.response_time = _log.response_time
                server.ipaddress = address
                server.last_checked = _log.datetime

            else:
                _log = ServerLog(
                    server_id=server.id,
                    datetime=datetime.now(),
                    url=server.domain_name,
                    error=server.status,
                )

                server.status = error

            session.add(_log)
            session.commit()
            session.refresh(server)
            session.refresh(_log)
            print(_log, flush=True)


while True:
    # iterates forever
    main_thread()
