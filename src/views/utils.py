import logging
from flask import jsonify

def arr_to_str(arr):
    return ", ".join(arr)

class ValidationError(Exception):
    def __init__(self, fields):
        self.message = f"Please provide values for: { arr_to_str(fields) }"

class IntegrityError(Exception):
    def __init__(self, message):
        self.message = message


def validate_dict(d, fields, validators={}):
    missing_fields = []
    result = {}

    for f in fields:
        if f not in d or ( f in validators and validators[f](d[f]) ):
            missing_fields.append(f)
        result[f] = d[f]

    if len(missing_fields) > 0:
        raise ValidationError(missing_fields)

    return result

def check_unique_constraint(model, fields_dict):
    if model.query.filter_by(**fields_dict).first() != None:
        raise IntegrityError("Unique constraint not met")
    return None

def error_response(message, code=500):
    logging.warning(message)
    return jsonify({ "msg": message }), code