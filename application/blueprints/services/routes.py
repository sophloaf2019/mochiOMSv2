from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from application.extensions import db
from application.blueprints.services.models import *


all_types = [
    "text",
    "textarea",
    "number",
    "float",
    "boolean",
    "date",
    "select"
]

services_bp = Blueprint('services', __name__, template_folder="templates", url_prefix='/services')

@services_bp.route('/', methods = ['get'])
def homepage():
    services = Service.query.filter_by(parent_service_id=None).all()
    
    return render_template('services_homepage.html', services = services, all_types = all_types)


@services_bp.route('/new', methods = ['POST'])
def new():
    
    data = request.form.to_dict()
    new_model = None
    type_select = data.get('type_select')
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
    new_model.parent_service_id = data.get('parent_service_id')
    db.session.add(new_model)
    db.session.commit()
    
    id = None
    if isinstance(new_model, Service):
        id = new_model.id
    else:
        id = new_model.parent_service_id
    
    return redirect(url_for('services.edit', id = id))

@services_bp.route('/<id>', methods = ['GET'])
def view(id):
    service = Service.query.get(id)
    if service:
        return render_template('services_view.html', service = service)
    else:
        flash('No service exists by that ID.', 'danger')
        return redirect(url_for('services.homepage'))

@services_bp.route('/<id>/edit', methods = ['GET'])
def edit(id):
    service = Service.query.get(id)
    if service:
        return render_template('services_edit.html', service = service, all_types = all_types)
    else:
        flash('No service exists by that ID.', 'danger')
        return redirect(url_for('services.homepage'))

def update_instance_fields(instance, data):
    """Helper function to update instance fields based on form data."""
    for key, value in data.items():
        if key == 'is_archived':
            value = value == 'True'  # Convert to boolean
        if hasattr(instance, key):
            setattr(instance, key, value)

@services_bp.route('/<id>/edit/save/<type_select>/<sub_id>', methods=['POST'])
@services_bp.route('/<id>/edit/save', methods=['POST'])
def save(id, type_select=None, sub_id=None):
    service = Service.query.get(id)
    data = request.form.to_dict()

    if not service:
        flash('No service under that ID.', 'danger')
        return redirect(url_for('services.homepage'))

    # Case 1: Updating the service itself (without type_select and sub_id)
    if type_select is None and sub_id is None:
        update_instance_fields(service, data)  # Use helper function
        db.session.commit()
        flash('Changes saved.', 'success')
        return redirect(url_for('services.edit', id=service.id))

    # Case 2: Updating an option based on type_select and sub_id
    if type_select in all_types and sub_id:
        # Dynamically map type_select to the correct model class
        option_classes = {
            "service": Service,
            "text": TextOption,
            "textarea": TextareaOption,
            "number": NumberOption,
            "float": FloatOption,
            "boolean": BooleanOption,
            "date": DateOption,
            "select": SelectOption
        }

        option_class = option_classes.get(type_select)
        if not option_class:
            flash('Invalid option type selected.', 'danger')
            return redirect(url_for('services.homepage'))

        option = option_class.query.get(sub_id)
        if not option:
            flash('No option under that ID.', 'danger')
            return redirect(url_for('services.homepage'))

        update_instance_fields(option, data)  # Use helper function
        db.session.commit()
        flash('Changes saved.', 'success')
        return redirect(url_for('services.edit', id=service.id))

    flash('Invalid request parameters.', 'danger')
    return redirect(url_for('services.homepage'))
