import os
import jwt
import time
import requests
from flask import abort
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import redirect
from flask import current_app
from flask import session
from urllib.parse import unquote
from base64 import b64encode
from datetime import datetime
from sqlmodel import select
from sqlmodel import Session as SQLSession
from app.models.user import User

bp = Blueprint("auth", __name__)


@bp.route("/login")
def login():
    CLIENT_ID = current_app.config["CLIENT_ID"]
    REDIRECT_URI = current_app.config["REDIRECT_URI"]
    USER_STATE = b64encode(os.urandom(64)).decode("utf-8")
    UAA_AUTHORIZE_URI = current_app.config["UAA_AUTHORIZE_URI"]

    session["USER_STATE"] = USER_STATE

    UAA_LOGIN = f"{UAA_AUTHORIZE_URI}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&state={USER_STATE}"

    return redirect(UAA_LOGIN)


@bp.route("/logout")
def logout():
    CLIENT_ID = current_app.config["CLIENT_ID"]
    REDIRECT_URI = current_app.config["REDIRECT_URI"]
    UAA_LOGOUT_URI = current_app.config["UAA_LOGOUT_URI"]
    UAA_LGOUT = f"{UAA_LOGOUT_URI}?client_id={CLIENT_ID}&redirect={REDIRECT_URI}"

    session.clear()
    requests.post(UAA_LGOUT)

    return redirect("/")


@bp.route("/callback")
def callback():
    # @url_param {string} code
    # @url_param {string} status
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        abort(400)

    UAA_TOKEN_URI = current_app.config["UAA_TOKEN_URI"]

    data = {
        "code": code,
        "grant_type": "authorization_code",
        "response_type": "token",
        "client_id": current_app.config["CLIENT_ID"],
        "client_secret": current_app.config["CLIENT_SECRET"],
        "redirect_uri": current_app.config["REDIRECT_URI"],
    }

    response = requests.post(UAA_TOKEN_URI, data=data)

    if response.status_code != 200:
        abort(response.status_code)

    response = response.json()

    token = response["access_token"]
    header = jwt.get_unverified_header(token)

    session["claims"] = jwt.decode(
        token, header["alg"], options={"verify_signature": False}
    )
    session["expiry"] = time.time() + (response["expires_in"] * 1000)
    session["refresh_token"] = response["refresh_token"]
    session["authenticated"] = True

    with SQLSession(current_app.engine) as s:
        query = select(User).where(User.email == session["claims"]["email"])
        user = s.exec(query).first()

        if user:
            # Account exists
            user.last_logon = datetime.now()
            s.add(user)
            s.commit()

        else:
            # Account does not exist
            new_user = User(
                user_name=session["claims"]["user_name"],
                email=session["claims"]["email"],
                last_logon=datetime.now(),
            )
            s.add(new_user)
            s.commit()

        user = s.exec(query).first()
        session["user"] = user.dict()

    return redirect("/")
