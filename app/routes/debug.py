from flask import Blueprint
from flask import request
from flask import jsonify
from flask import current_app
from app.utils.decorators import admin_required

bp = Blueprint("debug", __name__)


@bp.route("/headers")
@admin_required
def debug_headers():
    _tmp = {}
    for (
        h,
        v,
    ) in request.headers.items():
        _tmp[str(h)] = str(v)

    return jsonify(_tmp)


@bp.route("/env")
@admin_required
def debug_env():
    return jsonify(current_app.config["LOCAL_ENV"])
