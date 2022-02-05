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

bp = Blueprint("admin", __name__)


@bp.route("/")
@admin_required
def index():
    return render_markdown(
        "page.html",
        file="admin.md",
        session=session,
    )


@bp.route("/organizations", methods=["GET"])
def get_organizations():
    with SQLSession(current_app.engine) as s:
        orgs = select(Organization)
        results = s.exec(orgs).all()

        return render_template(
            "admin/organizations.html", session=session, organizations=results
        )


@bp.route("/server/organization", methods=["POST", "DELETE"])
def post_server():
    if request.method == "POST":
        data = request.form

        org_id = data.get("id").strip()
        title = data.get("title").strip()
        return jsonify({}), 200


@bp.route("/catagory", methods=["POST"])
def get_catagory():
    data = request.form

    cat_id = data.get("id")
    title = data.get("title")
    color = data.get("color")

    with SQLSession(current_app.engine) as s:
        if cat_id:
            _catagory = s.exec(select(Catagory).where(Catagory.id == cat_id)).one()
            _catagory.title = data.get("title")
            _catagory.meta_ref = data.get("title").lower().replace(" ", "-")
            _catagory.color = data.get("color")
            s.add(_catagory)
            s.commit()

        else:
            _catagory = Catagory(
                title=data.get("title"),
                meta_ref=data.get("title").lower().replace(" ", "-"),
                color=data.get("color"),
            )
            s.add(_catagory)
            s.commit()

    return jsonify({"result": "Operate successfully"})


@bp.route("/catagories", methods=["GET", "POST"])
def get_post_catagories():
    if request.method == "GET":
        with SQLSession(current_app.engine) as s:
            results = s.exec(select(Catagory)).all()

            return render_template(
                "admin/catagories.html", sesssion=session, catagories=results
            )
    else:
        data = request.get_json()
