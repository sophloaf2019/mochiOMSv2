from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from application.extensions import db
from application.blueprints.services.models import *


all_types = [
    TextOption.url_type,
    TextareaOption.url_type,
    NumberOption.url_type,
    FloatOption.url_type,
    BooleanOption.url_type,
    DateOption.url_type,
    SelectOption.url_type,
]

url_class_map = {
    Service.url_type: Service,
    TextOption.url_type: TextOption,
    TextareaOption.url_type: TextareaOption,
    NumberOption.url_type: NumberOption,
    FloatOption.url_type: FloatOption,
    BooleanOption.url_type: BooleanOption,
    DateOption.url_type: DateOption,
    SelectOption.url_type: SelectOption,
}


services_bp = Blueprint(
    "services", __name__, template_folder="templates", url_prefix="/services"
)


@services_bp.route("/", methods=["get"])
def homepage():
    services = Service.query.filter_by(parent_service_id=None).all()

    return render_template(
        "services_homepage.html", services=services, all_types=all_types
    )


@services_bp.route("/new", methods=["POST"])
def new():
    data = request.form.to_dict()
    new_model = None
    type_select = data.get("type_select")
    match type_select:
        case "service":
            new_model = Service()
        case "text":
            new_model = TextOption()
        case "textarea":
            new_model = TextareaOption()
        case "number":
            new_model = NumberOption()
        case "float":
            new_model = FloatOption()
        case "boolean":
            new_model = BooleanOption()
        case "date":
            new_model = DateOption()
        case "select":
            new_model = SelectOption()
    new_model.parent_service_id = data.get("parent_service_id")
    db.session.add(new_model)
    db.session.commit()

    id = None
    if isinstance(new_model, Service):
        id = new_model.id
    else:
        id = new_model.parent_service_id

    return redirect(url_for("services.edit", id=id))


@services_bp.route("/<url_type>/<id>", methods=["GET"])
def view(url_type, id):
    model = url_class_map.get(url_type).query.get(id)
    if model:
        return render_template("services_view.html", service=model)
    else:
        flash("Nothing of type " + model + " exists with ID " + str(id), "danger")
        return redirect(url_for("services.homepage"))


@services_bp.route("/<id>/edit", methods=["GET"])
def edit(url_type, id):
    model = url_class_map.get(url_type).query.get(id)
    if model:
        return render_template("services_edit.html", model=model, all_types=all_types)
    else:
        flash("Nothing of type " + model + " exists with ID " + str(id), "danger")
        return redirect(url_for("services.homepage"))


def update_instance_fields(instance, data):
    """Helper function to update instance fields based on form data."""
    for key, value in data.items():
        if key == "is_archived":
            value = value == "True"  # Convert to boolean
        if hasattr(instance, key):
            setattr(instance, key, value)


@services_bp.route("/<url_type>/<id>/edit/save", methods=["POST"])
def save(url_type, id):
    model = url_class_map.get(url_type).query.get(id)
    if model:
        return render_template("services_edit.html", model=model, all_types=all_types)
    data = request.form.to_dict()

    if not model:
        flash("No service under that ID.", "danger")
        return redirect(url_for("services.homepage"))

    update_instance_fields(model, data)  # Use helper function
    db.session.commit()
    flash("Changes saved.", "success")
    return redirect(url_for("services.edit", id=model.id))
