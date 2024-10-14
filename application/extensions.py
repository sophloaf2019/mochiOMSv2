from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask import render_template

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class FormModel:
    def to_form(self):
        form_html = ""
        
        for attr in self.form_attribute_list:
            value = getattr(self, attr)
            label = attr.capitalize()  # Capitalize the attribute name for the label
            
            # Determine the input type based on column type
            if isinstance(self.__table__.columns[attr].type, db.Integer):
                input_type = 'number'
                step = '1'
            elif isinstance(self.__table__.columns[attr].type, db.Float):
                input_type = 'number'
                step = '0.01'
            elif isinstance(self.__table__.columns[attr].type, db.String):
                input_type = 'text'
            elif isinstance(self.__table__.columns[attr].type, db.Text):
                input_type = 'textarea'
            elif isinstance(self.__table__.columns[attr].type, db.Boolean):
                input_type = 'checkbox'
                hidden_input = f'<input type="hidden" name="{attr}" value="False">'
                checkbox = f'<input type="checkbox" name="{attr}" value="True" {"checked" if value else ""}>'
                form_html += f'<label for="{attr}">{label}</label>{hidden_input}{checkbox}<br>'
                continue
            elif isinstance(self.__table__.columns[attr].type, db.DateTime):
                input_type = 'datetime-local'
            
            # Render the input field using Jinja
            form_html += render_template('form_controls.html', 
                                          attr=attr, 
                                          label=label, 
                                          value=value, 
                                          input_type=input_type, 
                                          step=step if 'step' in locals() else None)
        
        return form_html


# Create a single instance of SQLAlchemy to be used across the app
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
