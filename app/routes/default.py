import os
import time
import werkzeug
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import render_template
from flask import current_app
from flask import abort
from flask import json
from app.utils import render_markdown
from datetime import datetime
from base64 import b64encode
from sqlmodel import select
from sqlmodel import Session as SQLSession
from app.models.user import User
from app.models.server import Server, ServerLog
import jinja2
import psutil

bp = Blueprint("index", __name__)


@bp.route("/<path:path>")
def handle_posts(*args, **kwgs):
    if request.path in current_app.pages.registered:
        return render_markdown("page.html", session=session)

    abort(404)


@bp.route("/about")
def techstack(*args, **kwgs):

    return render_markdown(
        "page.html", file="techstack.md", session=session, time=datetime.now()
    )

    abort(404)


@bp.route("/")
def server(*args, **kwgs):

    with SQLSession(current_app.engine) as s:
        logs = select(ServerLog).order_by(ServerLog.id.desc()).limit(5)
        logs = s.exec(logs).all()

        down_logs = select(Server).where(Server.status == "DOWN")
        down_logs = s.exec(down_logs).all()

        popular_sites = select(Server).limit(25)

        popular_sites = s.exec(popular_sites).all()

    return render_template(
        "main/server.html", logs=logs, down_logs=down_logs, popular_sites=popular_sites
    )

    abort(404)


@bp.route("/server/<string:sitename>")
def get_server(sitename, *args, **kwgs):
    return sitename


@bp.before_request
def before_request():
    if session.get("expiry"):
        if time.time() > session.get("expiry"):
            # @url_param {string} code
            # @url_param {string} status
            UAA_TOKEN_URI = current_app.config["UAA_TOKEN_URI"]

            data = {
                "grant_type": "refresh_token",
                "refresh_token": session.get("refresh_token"),
                "client_id": current_app.config["CLIENT_ID"],
                "client_secret": current_app.config["CLIENT_SECRET"],
            }

            response = requests.post(UAA_TOKEN_URI, data=data).json()

            token = response["access_token"]
            header = jwt.get_unverified_header(token)

            session["claims"] = jwt.decode(
                token, header["alg"], options={"verify_signature": False}
            )
            session["expiry"] = time.time() + (response["expires_in"] * 1000)
            session["refresh_token"] = response["refresh_token"]
            session["authenticated"] = True


@bp.after_request
def after_request(response):
    current_app.count_requests += 1
    return response


def handle_exception(e):
    try:
        e.code
    except Exception:
        e.code = 500
        e.name = "Internal Server Error: {}".format(type(e).__name__)
        e.description = "{}".format(b64encode(str(e).encode("ascii")).decode("utf-8"))
    return render_template("error.html", error=e)
