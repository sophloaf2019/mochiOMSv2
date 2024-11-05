from application.extensions import db, FormModel
from sqlalchemy.orm import backref


"""

This file contains all models relevant to the service customization functionality of mochiOMS.

Explanations of each class's functionality are in their docstrings.

Current classes:
    Service
    TextOption
    TextareaOption
    NumberOption
    SelectOption
    MultiselectOption
    SelectableOption
    FileOption

    
Note that each class also has an attribute called 'form_attribute_list'. This is a dictionary where the attribute name is a key,
and the attribute type is a value. This is necessary for the FormModel class defined in extensions.py, which simplifies CRUD operations.
Only define attributes in here that you want to be editable -- so *not* ID.

"""


class Service(db.Model, FormModel):
    """

    Represents the greater service 'category'. Can contain children.

    id = primary key. autoincrements.
    name = the name of the category, like Printing or Cakes
    description = a description of the category
    price = the customer-facing intrinsic price of this category, to set an effective minimum price
    cost = same thing but business-facing cost
    is_archived = soft-deletes for Services
    total_cost = total costs incurred by the category
    revenue = total money earned from it

    various relationships = stores connections to other Services and available options
    """

    __tablename__ = "services"

    form_attribute_list = {
        "name": "text",
        "description": "textarea",
        "price": "float",
        "cost": "float",
        "is_archived": "boolean",
        "total_cost": "float",
        "revenue": "float",
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, default="New Service")
    description = db.Column(
        db.Text, nullable=True, default="This is the description for your new service."
    )
    price = db.Column(db.Float, nullable=False, default=0)
    cost = db.Column(db.Float, nullable=False, default=0)
    is_archived = db.Column(db.Boolean, nullable=True, default=False)
    total_cost = db.Column(db.Float, nullable=True, default=0)
    revenue = db.Column(db.Float, nullable=True, default=0)

    parent_service_id = db.Column(
        db.Integer, db.ForeignKey("services.id"), nullable=True, default=None
    )

    # Relationship for child services (points to other Service rows)
    child_services = db.relationship(
        "Service",
        backref=db.backref("parent_service", remote_side=[id]),
        lazy=True,
        cascade="all, delete-orphan",
    )
    text_options = db.relationship(
        "TextOption", backref="parent_service", lazy=True, cascade="all, delete-orphan"
    )
    textarea_options = db.relationship(
        "TextareaOption",
        backref="parent_service",
        lazy=True,
        cascade="all, delete-orphan",
    )
    number_options = db.relationship(
        "NumberOption",
        backref="parent_service",
        lazy=True,
        cascade="all, delete-orphan",
    )
    float_options = db.relationship(
        "FloatOption", backref="parent_service", lazy=True, cascade="all, delete-orphan"
    )
    boolean_options = db.relationship(
        "BooleanOption",
        backref="parent_service",
        lazy=True,
        cascade="all, delete-orphan",
    )
    date_options = db.relationship(
        "DateOption", backref="parent_service", lazy=True, cascade="all, delete-orphan"
    )
    select_options = db.relationship(
        "SelectOption",
        backref="parent_service",
        lazy=True,
        cascade="all, delete-orphan",
    )

    inventory_id = db.Column(
        db.Integer, db.ForeignKey("inventory.id", ondelete="SET NULL"), nullable=True
    )
    inventory = db.relationship("Inventory", back_populates="services")
    inventory_multiplier = db.Column(db.Float, nullable=True, default=1)

    @property
    def all_field_children(self):
        return (
            self.text_options
            + self.textarea_options
            + self.number_options
            + self.float_options
            + self.boolean_options
            + self.date_options
            + self.select_options
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "cost": self.cost,
            "is_archived": self.is_archived,
            "total_cost": self.total_cost,
            "revenue": self.revenue,
            "child_services": [child.to_dict() for child in self.child_services],
            "text_options": [child.to_dict() for child in self.text_options],
            "textarea_options": [child.to_dict() for child in self.textarea_options],
            "number_options": [child.to_dict() for child in self.number_options],
            "float_options": [child.to_dict() for child in self.float_options],
            "boolean_options": [child.to_dict() for child in self.boolean_options],
            "date_options": [child.to_dict() for child in self.date_options],
            "inventory": self.inventory.name,
            "inventory_multiplier": self.inventory_multiplier,
        }

    url_type = "service"


class Option(db.Model, FormModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, default="New Option")
    notes = db.Column(
        db.Text, nullable=True, default="These are the notes for your new option."
    )
    # price = db.Column(db.Float, nullable=False)
    # cost = db.Column(db.Float, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    parent_service_id = db.Column(
        db.Integer, db.ForeignKey("services.id"), nullable=False
    )

    form_attribute_list = {
        "name": "text",
        "notes": "textarea",
        "is_archived": "boolean",
    }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "notes": self.notes,
            "is_archived": self.is_archived,
        }


class TextOption(Option):
    __tablename__ = "text_options"

    minimum_length = db.Column(db.Integer, nullable=True)
    maximum_length = db.Column(db.Integer, nullable=True)
    default_value = db.Column(db.String, nullable=True)

    form_attribute_list = {
        **Option.form_attribute_list,
        "minimum_length": "number",
        "maximum_length": "number",
        "default_value": "text",
    }

    def to_dict(self):
        data = super().to_dict()

        data.update(
            {
                "minimum_length": self.minimum_length,
                "maximum_length": self.maximum_length,
                "default_value": self.default_value,
            }
        )
        return data

    url_type = "text"


class TextareaOption(Option):
    __tablename__ = "textarea_options"

    minimum_length = db.Column(db.Integer, nullable=True)
    maximum_length = db.Column(db.Integer, nullable=True)
    default_value = db.Column(db.String, nullable=True)

    form_attribute_list = {
        **Option.form_attribute_list,
        "minimum_length": "number",
        "maximum_length": "number",
        "default_value": "text",
    }

    def to_dict(self):
        data = super().to_dict()

        data.update(
            {
                "minimum_length": self.minimum_length,
                "maximum_length": self.maximum_length,
                "default_value": self.default_value,
            }
        )
        return data

    url_type = "textarea"


class NumberOption(Option):
    __tablename__ = "number_options"

    minimum = db.Column(db.Integer, nullable=True)
    maximum = db.Column(db.Integer, nullable=True)
    step = db.Column(db.Integer, nullable=False, default=1)
    default_value = db.Column(db.Integer, nullable=True)

    form_attribute_list = {
        **Option.form_attribute_list,
        "minimum": "number",
        "maximum": "number",
        "step": "number",
        "default_value": "number",
    }

    def to_dict(self):
        data = super().to_dict()

        data.update(
            {
                "minimum": self.minimum,
                "maximum": self.maximum,
                "step": self.step,
                "default_value": self.default_value,
            }
        )
        return data

    url_type = "number"


class FloatOption(Option):
    __tablename__ = "float_options"

    minimum = db.Column(db.Float, nullable=True)
    maximum = db.Column(db.Float, nullable=True)
    step = db.Column(db.Float, nullable=False, default=1)
    default_value = db.Column(db.Float, nullable=True)

    form_attribute_list = {
        **Option.form_attribute_list,
        "minimum": "float",
        "maximum": "float",
        "step": "float",
        "default_value": "float",
    }

    def to_dict(self):
        data = super().to_dict()

        data.update(
            {
                "minimum": self.minimum,
                "maximum": self.maximum,
                "step": self.step,
                "default_value": self.default_value,
            }
        )
        return data

    url_type = "float"


class BooleanOption(Option):
    __tablename__ = "boolean_options"

    default_value = db.Column(db.Boolean, nullable=True)

    form_attribute_list = {**Option.form_attribute_list, "default_value": "boolean"}

    def to_dict(self):
        data = super().to_dict()

        data.update({"default_value": self.default_value})
        return data

    url_type = "boolean"


class DateOption(Option):
    __tablename__ = "date_options"

    default_value = db.Column(db.DateTime, nullable=True)
    enforce_future_date = db.Column(db.Boolean, nullable=True)

    form_attribute_list = {
        **Option.form_attribute_list,
        "default_value": "datetime-local",
        "enforce_future_date": "boolean",
    }

    def to_dict(self):
        data = super().to_dict()

        data.update(
            {
                "default_value": self.default_value,
                "enforce_future_date": self.enforce_future_date,
            }
        )
        return data

    url_type = "date"


class SelectOption(Option):
    __tablename__ = "select_options"

    # Define the foreign key for the selectables relationship
    selectables = db.relationship(
        "Selectable",
        back_populates="select_option",
        foreign_keys="Selectable.select_option_id",  # Use this foreign key
    )

    # Foreign key for default_value relationship
    default_value_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "selectables.id", name="fk_select_options_selectables", use_alter=True
        ),
        nullable=True,
    )
    default_value = db.relationship("Selectable", foreign_keys=[default_value_id])

    def to_dict(self):
        data = super().to_dict()

        data.update(
            {
                "selectables": [child.to_dict() for child in self.selectables],
                "default_value": self.default_value.to_dict(),
            }
        )
        return data

    url_type = "select"


class Selectable(db.Model, FormModel):
    __tablename__ = "selectables"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="New Selectable")
    price = db.Column(db.Float, nullable=False, default=0)
    cost = db.Column(db.Float, nullable=False, default=0)

    # Foreign key back to SelectOption
    select_option_id = db.Column(
        db.Integer,
        db.ForeignKey("select_options.id", name="fk_selectables_select_options"),
        nullable=False,
    )
    select_option = db.relationship(
        "SelectOption",
        back_populates="selectables",
        foreign_keys=[select_option_id],  # Specify the foreign key
    )

    # Inventory relationship
    inventory_id = db.Column(
        db.Integer, db.ForeignKey("inventory.id", ondelete="SET NULL"), nullable=True
    )
    inventory = db.relationship("Inventory", back_populates="selectables")
    inventory_multiplier = db.Column(db.Float, nullable=True)

    form_attribute_list = {
        "name": "text",
        "price": "float",
        "cost": "float",
    }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "cost": self.cost,
            "inventory": self.inventory.name,
            "inventory_multiplier": self.inventory_multiplier,
        }

    url_type = "selectable"
