"""

Takes a dictionary of data and an instance and updates values of the model according to
my defined data validation practices.

Currently, there are none in place, besides a simple try/except for errors (like accidentally submitting
a string to a numerical-only field).

"""

from application.extensions import str_to_obj, db

def update_instance_fields(instance, data):
    try:
        for key, value in data.items():
            data[key] = str_to_obj(value)
            if key == "delete" and data[key] == True:
                db.session.delete(instance)
                db.session.commit()
                return None
            print(key, data[key])
            if hasattr(instance, key):
                setattr(instance, key, data[key])
        db.session.commit()
        
        return True
    except Exception as e:
        db.session.rollback()
        return False
    