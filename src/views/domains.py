import json
import logging
from flask import Blueprint, jsonify, request
from ..models import Domain, Annotation, db
from .utils import ValidationError, validate_dict, check_unique_constraint, IntegrityError, error_response

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
            return error_response("The domain already exists", 400)
        except ValidationError as ve:
            return error_response(ve.message, 400)
        except Exception as e:
            return error_response(e.message)
    
    return jsonify([ item.to_json() for item in Domain.query.all() ]), 200

@bp.route("/<int:domain_id>")
def show_domain_annotations(domain_id):
    try:
        domain = Domain.query.filter_by(id=domain_id).first()

        if domain == None:
            return "Not found", 404
        
        return jsonify({ "annotations": [ anno.to_json(exclude=["url", "domain"]) for anno in domain.annotations ], **domain.to_json()})
    except Exception as e:
        return error_response(e.message)
