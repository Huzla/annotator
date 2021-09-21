import json
import logging
from flask import Blueprint, jsonify, request
from ..models import Domain, Annotation, db
from .utils import ValidationError, validate_dict, check_unique_constraint, IntegrityError

bp = Blueprint("domains", __name__, url_prefix="/domains")

@bp.route("", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        try:
            obj = json.loads(request.data)

            valid_dict = validate_dict(obj, ["name", "index_page"])

            check_unique_constraint(Domain, valid_dict)
            
            db.session.add(Domain(**valid_dict))
            db.session.commit()

            return "Done", 200
        except IntegrityError:
            logging.warning(f"Domain unique constriant not met by: { obj }")
            return jsonify({ "msg": "The domain already exists" }), 400
        except ValidationError:
            logging.warning(f"Invalid domain insert: { valid_dict }")
            return jsonify({ "msg": valid_dict.message }), 400
        except Exception as e:
            logging.error(e)
            return jsonify({ "msg": "Internal server error" }), 500
    
    return jsonify([ item.to_json() for item in Domain.query.all() ]), 200