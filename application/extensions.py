from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask import render_template, Blueprint
from termcolor import cprint


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

        for attr, input_type in self.form_attribute_list.items():
            value = getattr(self, attr)
            label = attr.replace("_", " ").title()
            step = "1"
            # number, float, text, textarea, checkbox
            if input_type == "float":
                input_type = "number"
                step = "0.01"
            if input_type == "boolean":
                input_type = "checkbox"
            form_html += render_template(
                "form_controls.html",
                attr=attr,
                label=label,
                value=value,
                input_type=input_type,
                step=step,
            )

        return form_html


# custom templates for filtering stuff in Jinja

filters_bp = Blueprint("filters", __name__)


@filters_bp.app_template_filter("snake_to_upper")
def snake_to_upper(text):
    list_of_words = text.split("_")
    list_of_words = [word.capitalize() for word in list_of_words]
    new_text = " ".join(list_of_words)
    return new_text

def str_to_obj(text: str):
    
    # try to convert to a boolean
    if text == 'True':
        return True
    if text == 'False':
        return False
    
    # try to convert to a null value
    if text == "":
        return None
    
    # try to convert to an integer
    try:
        return int(text)
    except:
        pass
    
    # try to convert to a float
    try:
        return float(text)
    except:
        pass
    
    return text

# Create a single instance of SQLAlchemy to be used across the app
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

# unit testing
if __name__ == "__main__":
    assert str_to_obj("True") == True
    assert str_to_obj("False") == False
    assert str_to_obj("") == None
    assert str_to_obj("123") == 123
    assert str_to_obj("1.23") == 1.23
    assert str_to_obj("String") == "String"
    print("All tests for str_to_obj() passed.")