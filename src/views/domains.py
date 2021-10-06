import json
import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from ..models import Domain, Annotation, db
from .utils import ValidationError, validate_dict, check_unique_constraint, IntegrityError, error_response

bp = Blueprint("domains", __name__, url_prefix="/domains")

CORS(bp)

@bp.route("", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        try:
            obj = json.loads(request.data)

            valid_dict = validate_dict(obj, ["name", "index_page"])

            check_unique_constraint(Domain, valid_dict)
            
            new_domain = Domain(**valid_dict)

            db.session.add(new_domain)
            db.session.commit()

            return jsonify(new_domain.to_json()), 201
        except IntegrityError:
            return error_response("The domain already exists", 400)
        except ValidationError as ve:
            return error_response(ve.message, 400)
        except Exception as e:
            return error_response(str(e))
    
    logging.info([ item.to_json() for item in Domain.query.all() ])
    return jsonify([ item.to_json() for item in Domain.query.all() ]), 200

@bp.route("/<int:domain_id>", methods=("GET", "POST"))
def show_domain_annotations(domain_id):
    try:

        domain = Domain.query.filter_by(id=domain_id).first()

        if domain == None:
            return "Not found", 404
        
        if request.method == "POST":
            try:
                obj = json.loads(request.data)

                valid_dict = validate_dict(obj, ["url", "group", "classes", "document"], { "url": lambda u: u == "", "classes": lambda c: len(c) == 0 })

                anno = Annotation.query.filter_by(url=valid_dict["url"], domain=domain_id).first()
                

                if anno == None:
                    if valid_dict["group"] < 0:
                        raise ValidationError(["group"])
                    anno = Annotation(domain=domain_id, url=valid_dict["url"], group=valid_dict["group"], classes=",".join(valid_dict["classes"]))
                else:
                    anno.group = valid_dict["group"]
                    anno.classes = ",".join(valid_dict["classes"])

                if anno.group > domain.groups:
                    domain.groups = anno.group
                    db.session.add(domain)

                db.session.add(anno)
                db.session.commit()


            except ValidationError as ve:
                return error_response(ve.message, 400)
            except Exception as e:
                return error_response(str(e))        


        
        return jsonify({ "annotations": [ anno.to_json(exclude=["domain"]) for anno in domain.annotations ], **domain.to_json()})
    except Exception as e:
        return error_response(str(e))

@bp.route("/<int:domain_id>/<int:annotation_id>")
def show_annotation(domain_id, annotation_id):
    try:
        domain = Domain.query.filter_by(id=domain_id).first()
        annotation = Annotation.query.filter_by(id=annotation_id, domain=domain_id).first()

        if domain == None or annotation == None:
            return "Not found", 404

        return jsonify({ **annotation.to_json(exclude=["domain"]), "domain": domain.to_json(exclude=["annotations", "id"]) })
       
    except Exception as e:
        return error_response(str(e))