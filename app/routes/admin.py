from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import current_app
from app.utils import render_markdown
from app.utils.decorators import admin_required

bp = Blueprint("admin", __name__)


@bp.route("/")
@admin_required
def index():
    return render_markdown(
        "page.html",
        file="admin.md",
        session=session,
    )


@bp.route("/logs")
def logs():
    return render_template("log.html", sesssion=session)
