from application.extensions import db
from sqlalchemy.orm import backref


class ParentOrder(db.Model):

    __tablename__ = "parent_orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_archived = db.Column(db.Boolean, nullable=True, default=False)
    child_services = db.relationship("OrderService", backref="parent_order", lazy=True)
    due_date = db.Column(db.DateTime, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)


class OrderService(db.Model):
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

    __tablename__ = "order_services"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=True, default=False)

    parent_order_id = db.Column(
        db.Integer, db.ForeignKey("parent_orders.id"), nullable=True
    )

    service_id = db.Column(
        db.Integer, db.ForeignKey("order_services.id"), nullable=True
    )
    child_services = db.relationship(
        "OrderService", backref=backref("parent_service", remote_side=[id]), lazy=True
    )
    text_order_options = db.relationship(
        "TextOrderOption", backref="parent_service", lazy=True
    )
    textarea_order_options = db.relationship(
        "TextareaOrderOption", backref="parent_service", lazy=True
    )
    number_order_options = db.relationship(
        "NumberOrderOption", backref="parent_service", lazy=True
    )
    float_order_options = db.relationship(
        "FloatOrderOption", backref="parent_service", lazy=True
    )
    boolean_order_options = db.relationship(
        "BooleanOrderOption", backref="parent_service", lazy=True
    )
    date_order_options = db.relationship(
        "DateOrderOption", backref="parent_service", lazy=True
    )

    inventory_id = db.Column(
        db.Integer, db.ForeignKey("inventory.id", ondelete="SET NULL"), nullable=True
    )
    inventory = db.relationship("Inventory", back_populates="order_services")
    inventory_multiplier = db.Column(db.Float, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)


class OrderOption(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    # price = db.Column(db.Float, nullable=False)
    # cost = db.Column(db.Float, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    service_id = db.Column(
        db.Integer, db.ForeignKey("order_services.id"), nullable=True
    )


class TextOrderOption(OrderOption):
    __tablename__ = "text_order_options"

    minimum_length = db.Column(db.Integer, nullable=True)
    maximum_length = db.Column(db.Integer, nullable=True)
    value = db.Column(db.String, nullable=True)


class TextareaOrderOption(OrderOption):
    __tablename__ = "textarea_order_options"

    minimum_length = db.Column(db.Integer, nullable=True)
    maximum_length = db.Column(db.Integer, nullable=True)
    value = db.Column(db.String, nullable=True)


class NumberOrderOption(OrderOption):
    __tablename__ = "number_order_options"

    minimum = db.Column(db.Integer, nullable=True)
    maximum = db.Column(db.Integer, nullable=True)
    step = db.Column(db.Integer, nullable=False, default=1)
    value = db.Column(db.Integer, nullable=True)


class FloatOrderOption(OrderOption):
    __tablename__ = "float_order_options"

    minimum = db.Column(db.Float, nullable=True)
    maximum = db.Column(db.Float, nullable=True)
    step = db.Column(db.Float, nullable=False, default=1)
    value = db.Column(db.Float, nullable=True)


class BooleanOrderOption(OrderOption):
    __tablename__ = "boolean_order_options"

    value = db.Column(db.Boolean, nullable=True)


class DateOrderOption(OrderOption):
    __tablename__ = "date_order_options"

    value = db.Column(db.DateTime, nullable=True)
    enforce_future_date = db.Column(db.Boolean, nullable=True)


class SelectOrderOption(OrderOption):
    __tablename__ = "select_order_options"

    selectables = db.relationship(
        "OrderSelectable", back_populates="select_order_option"
    )
    value_id = db.Column(
        db.Integer, db.ForeignKey("order_selectables.id", use_alter=True), nullable=True
    )
    value = db.relationship(
        "OrderSelectable", foreign_keys=[value_id], backref="value_for"
    )


class OrderSelectable(db.Model):
    __tablename__ = "order_selectables"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    select_option_id = db.Column(
        db.Integer, db.ForeignKey("select_options.id"), nullable=False
    )
    select_option = db.relationship("SelectOrderOption", back_populates="selectables")

    inventory_id = db.Column(
        db.Integer, db.ForeignKey("inventory.id", ondelete="SET NULL"), nullable=True
    )
    inventory = db.relationship("Inventory", back_populates="order_selectables")
    inventory_multiplier = db.Column(db.Float, nullable=True)
    select_order_option = db.relationship(
        "SelectOrderOption", back_populates="selectables"
    )
