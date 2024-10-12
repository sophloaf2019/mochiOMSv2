from application.extensions import db
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

"""


class Service(db.Model):
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=True, default=False)
    total_cost = db.Column(db.Integer, nullable=True)
    revenue = db.Column(db.Integer, nullable=True)

    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=True)
    child_services = db.relationship("Service", backref="parent_service", lazy=True)
    text_options = db.relationship("TextOption", backref="parent_service", lazy=True)
    textarea_options = db.relationship(
        "TextareaOption", backref="parent_service", lazy=True
    )
    number_options = db.relationship(
        "NumberOption", backref="parent_service", lazy=True
    )
    float_options = db.relationship("FloatOption", backref="parent_service", lazy=True)
    boolean_options = db.relationship(
        "BooleanOption", backref="parent_service", lazy=True
    )
    date_options = db.relationship("DateOption", backref="parent_service", lazy=True)

    # inventory_id = db.Column(
    #     db.Integer, db.ForeignKey("inventory.id", ondelete="SET NULL"), nullable=True
    # )
    # inventory = db.relationship("Inventory", back_populates="selectables")
    # inventory_multiplier = db.Column(db.Float, nullable=True)


class Option(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    # price = db.Column(db.Float, nullable=False)
    # cost = db.Column(db.Float, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=True)


class TextOption(Option):
    __tablename__ = "text_options"

    minimum_length = db.Column(db.Integer, nullable=True)
    maximum_length = db.Column(db.Integer, nullable=True)
    default_value = db.Column(db.String, nullable=True)


class TextareaOption(Option):
    __tablename__ = "textarea_options"

    minimum_length = db.Column(db.Integer, nullable=True)
    maximum_length = db.Column(db.Integer, nullable=True)
    default_value = db.Column(db.String, nullable=True)


class NumberOption(Option):
    __tablename__ = "number_options"

    minimum = db.Column(db.Integer, nullable=True)
    maximum = db.Column(db.Integer, nullable=True)
    step = db.Column(db.Integer, nullable=False, default=1)
    default_value = db.Column(db.Integer, nullable=True)


class FloatOption(Option):
    __tablename__ = "float_options"

    minimum = db.Column(db.Float, nullable=True)
    maximum = db.Column(db.Float, nullable=True)
    step = db.Column(db.Float, nullable=False, default=1)
    default_value = db.Column(db.Float, nullable=True)


class BooleanOption(Option):
    __tablename__ = "boolean_options"

    default_value = db.Column(db.Boolean, nullable=True)


class DateOption(Option):
    __tablename__ = "date_options"

    default_value = db.Column(db.DateTime, nullable=True)
    enforce_future_date = db.Column(db.Boolean, nullable=True)


class SelectOption(Option):
    __tablename__ = "select_options"

    selectables = db.relationship("Selectable", back_populates="select_option")
    default_value_id = db.Column(
        db.Integer, db.ForeignKey("selectables.id", use_alter=True), nullable=True
    )
    default_value = db.relationship(
        "Selectable", foreign_keys=[default_value_id], backref="default_for"
    )


class Selectable(db.Model):
    __tablename__ = "selectables"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    select_option_id = db.Column(
        db.Integer, db.ForeignKey("select_options.id"), nullable=False
    )
    select_option = db.relationship("SelectOption", back_populates="selectables")
