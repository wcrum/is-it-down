from flask import request
from flask import session
from flask import jsonify
from flask import abort
from sqlmodel import select
from sqlmodel import Session as SQLSession
from app.models.user import User
from flask import current_app


def admin_required(f):
    def wrapper(*args, **kwgs):
        user = session.get("user", {})
        if user.get("access") == "Administrator":
            return f(*args, **kwgs)
        return abort(401)

    wrapper.__name__ = f.__name__
    return wrapper


def login_required(f):
    def wrapper(*args, **kwgs):
        user = session.get("user", {})
        if user:
            return f(*args, **kwgs)
        return abort(401)

    return wrapper
