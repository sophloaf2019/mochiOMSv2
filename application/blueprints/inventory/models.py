from application.extensions import db


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    internal_sku = db.Column(db.String, nullable=True)
    external_sku = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)

    tagstring = db.Column(db.String, nullable=True)

    def gettagstring(self):
        return self.tagstring.split(",")

    def settagstring(self, value: list):
        self.tagstring = ",".join(value)

    def deltagstring(self):
        del self.tagstring

    tags = property(gettagstring, settagstring, deltagstring)

    cost = db.Column(db.Float)
    total_cost = db.Column(db.Float, default=0)

    location = db.Column(db.String, nullable=True)
    quantity = db.Column(db.Integer, default=0)
    amount_per_box = db.Column(db.Integer, default=0)
    minimum_level = db.Column(db.Integer)
    maximum_level = db.Column(db.Integer)
    days_to_receive = db.Column(db.Integer)

    weight = db.Column(db.Float, nullable=True)
    weight_unit = db.Column(db.String, nullable=True, default="lbs")
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    depth = db.Column(db.Float, nullable=True)
    dimensional_unit = db.Column(db.String, nullable=True, default="in")

    order_services = db.relationship(
        "OrderService",
        back_populates="inventory",
        foreign_keys="OrderService.inventory_id",
    )
    services = db.relationship("Service", back_populates="inventory")
    order_selectables = db.relationship("OrderSelectable", back_populates="inventory")
    selectables = db.relationship("Selectable", back_populates="inventory")

    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    is_archived = db.Column(db.Boolean, default=False)


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    representative_name = db.Column(db.String, nullable=True)

    items = db.relationship("Inventory", backref="supplier")

    is_archived = db.Column(db.Boolean, default=False)
