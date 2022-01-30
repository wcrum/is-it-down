from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from app.utils.decorators import admin_required

bp = Blueprint("user", __name__)


@bp.route("/<string:username>")
def user_profile(username):
    abort(500)
    return f"{username}"
