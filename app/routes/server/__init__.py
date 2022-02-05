from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import current_app
from flask import render_template
from flask import request
from app.utils import render_markdown
from sqlmodel import Session as SQLSession
from sqlmodel import select

from app.models.server import Catagory, Organization
from app.utils.decorators import admin_required
from app.models.user import User
from app.models.server import Server, ServerLog, Catagory, ServerReport
from datetime import datetime, timedelta

bp = Blueprint("server", __name__)


@bp.route("/organization", methods=["POST", "DELETE"])
def post_server():
    if request.method == "POST":
        data = request.form

        org_id = data.get("id").strip()
        title = data.get("title").strip()
        return jsonify({}), 200


@bp.route("/<string:sitename>")
def get_server(sitename, *args, **kwgs):
    with SQLSession(current_app.engine) as s:
        result = s.exec(select(Server).where(Server.domain_name == sitename)).first()
        result.clicks += 1
        s.add(result)
        s.commit()
        s.refresh(result)
        
        logs = s.exec(
            select(ServerLog).where(ServerLog.server_id == result.id).limit(10)
        ).all()

        server = type("data", (object,), {})()
        server.server = result
        server.catagories = result.catagories
        server.logs = logs
        server.organizations = result.organizations



    return render_template("main/server.html", session=session, server=server)


@bp.route("/<string:sitename>/reports")
def get_server_reports(sitename, *args, **kwgs):
    DATE_TIME_STRING_FORMAT = "%Y-%m-%dT%H:00:00"

    now = datetime.now()
    last_week = now - timedelta(days=7)

    with SQLSession(current_app.engine) as s:
        result = s.exec(select(Server).where(Server.domain_name == sitename)).first()
        statement = f"SELECT date_format( `datetime`, '{DATE_TIME_STRING_FORMAT}' ) as dt, count( id ) FROM  serverreport WHERE server_id = {result.id} GROUP BY dt"
        result = s.execute(statement).all()

        data = {}

        iter_date = last_week
        while iter_date <= now:
            data[iter_date.strftime(DATE_TIME_STRING_FORMAT)] = 0
            iter_date += timedelta(hours=1)

        for r in result:
            r = list(r)
            if (
                not (r_day := datetime.strptime(r[0], DATE_TIME_STRING_FORMAT))
                < last_week
            ):
                data[r_day.strftime(DATE_TIME_STRING_FORMAT)] = r[1]

        data = [[x, y] for x, y in data.items()]
    return jsonify(data)


@bp.route("/<string:sitename>/report", methods=["POST"])
def post_server_report(sitename, *args, **kwgs):
    now = datetime.now()
    with SQLSession(current_app.engine) as s:
        result = s.exec(select(Server).where(Server.domain_name == sitename)).first()
        report = ServerReport(datetime=now, server_id=result.id)
        s.add(report)
        s.commit()

    return jsonify({"code": 200, "description": "Added report."})
