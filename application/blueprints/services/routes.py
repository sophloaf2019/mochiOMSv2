from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from application.extensions import db, catalog, jp
from application.blueprints.services.models import *
from termcolor import cprint
from application.blueprints.services.data_validation import update_instance_fields


# An easy-to-find list of all available configurable options.
# Notably, Service is not present. The user gets a separate button for that.
all_types = [
    TextOption.url_type,
    TextareaOption.url_type,
    NumberOption.url_type,
    FloatOption.url_type,
    BooleanOption.url_type,
    DateOption.url_type,
    SelectOption.url_type,
]

# The URL class map is key for functionality in URLs.
# Since mochiOMS v2 has multiple tables for different option types,
# we can't guarantee the ID is unique.
# So, we create a url map. The URL will contain an attribute called
# 'url_type'.
# This dictionary performs on a lookup on this map and perform a query using the second URL piece,
# 'id'.
# So,
# Service.url_type is 'service'. We have a url coming in that's /service/1, which is mapped to the view() function.
# The dictionary looks up the word 'service' and finds it's related to the Service class. It performs a query on Service
# with the ID 1 and passes that to the Jinja template. Clever!

url_class_map = {
    Service.url_type: Service,
    TextOption.url_type: TextOption,
    TextareaOption.url_type: TextareaOption,
    NumberOption.url_type: NumberOption,
    FloatOption.url_type: FloatOption,
    BooleanOption.url_type: BooleanOption,
    DateOption.url_type: DateOption,
    SelectOption.url_type: SelectOption,
    Selectable.url_type: Selectable,
}


services_bp = Blueprint(
    "services", __name__, template_folder="templates", url_prefix="/services"
)


@services_bp.route("/", methods=["get"])
@services_bp.route("/<url_type>/<id>", methods=["get"])
def homepage(url_type=None, id=None):
    if url_type and id:
        model = url_class_map.get(url_type).query.get(id)
    else:
        model = None
    services = Service.query.filter_by(parent_service_id=None).all()

    return jp.render("services_homepage.html", model=model, services=services)


@services_bp.route("/new", methods=["POST"])
def new():
    data = request.form.to_dict()
    model = url_class_map.get(data.get("type_select"))()
    if hasattr(model, "parent_service_id"):
        model.parent_service_id = data.get("parent_service_id")
    elif hasattr(model, "select_option_id"):
        model.select_option_id = data.get("select_option_id")
    db.session.add(model)
    db.session.commit()

    return redirect(request.referrer)


@services_bp.route("/<url_type>/<id>/panel", methods=["GET"])
def panel(url_type, id):
    model = url_class_map.get(url_type).query.get(id)
    if model:
        return jp.render("services_view.html", service=model)
    else:
        flash(
            "Nothing of type '" + url_type + "' exists with ID " + str(id) + ".",
            "danger",
        )
        return redirect(url_for("services.homepage"))


@services_bp.route("/<url_type>/<id>/edit", methods=["GET"])
def edit(url_type, id):
    model = url_class_map.get(url_type).query.get(id)
    if model:
        return jp.render("services_edit.html", model=model, all_types=all_types)
    else:
        flash("Nothing of type " + model + " exists with ID " + str(id), "danger")
        return redirect(url_for("services.homepage"))


@services_bp.route("/<url_type>/<id>/edit/save", methods=["POST"])
def save(url_type, id):
    data = request.form.to_dict()
    model = url_class_map.get(url_type).query.get(id)
    if model:
        result = update_instance_fields(model, data)
        if result == True:
            flash("Changes saved.", "success")
            return redirect(
                url_for("services.edit", id=model.id, url_type=model.url_type)
            )
        elif result == False:
            flash("Something went wrong.", "danger")
            return redirect(
                url_for("services.edit", id=model.id, url_type=model.url_type)
            )
        elif result == None:
            flash("Content deleted.", "success")
            return redirect(url_for("services.homepage"))

    if not model:
        flash("No service under that ID.", "danger")
        return redirect(url_for("services.homepage"))

    return redirect(url_for("services.edit", id=model.id, url_type=model.url_type))


@services_bp.route("/search")
def search():
    # Get the "search" parameter from the query string
    search_term = request.args.get("search", "")

    # Get the "limit" parameter or default to 100 if it doesn't exist
    limit = int(request.args.get("limit", 100))

    # Query the Services model, filtering by name
    query = Service.query.filter(Service.name.ilike(f"%{search_term}%")).limit(limit)

    # Execute the query to get the results
    results = query.all()

    # Render the results in the 'services_table.html' template
    return jp.render("services_table.html", results=results)
