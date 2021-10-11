import json
import logging
from flask import Blueprint, jsonify, request, render_template_string
from flask_cors import CORS
from ..models import Domain, Annotation, db
from .utils import ValidationError, validate_dict, check_unique_constraint, IntegrityError, error_response
import urllib.request
from bs4 import BeautifulSoup


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
    
    return jsonify([ { **item.to_json(), "annotations": Annotation.query.filter_by(domain=item.id).count() } for item in Domain.query.all() ]), 200

@bp.route("/<int:domain_id>", methods=("GET", "POST"))
def show_domain(domain_id):
    try:

        domain = Domain.query.filter_by(id=domain_id).first()

        if domain == None:
            return "Not found", 404

        if request.method == "POST":
            try:
                obj = json.loads(request.data)
                
                valid_dict = validate_dict(obj, ["url", "group", "classes", "document"], { "url": lambda u: u == "" })

                anno = Annotation.query.filter_by(url=valid_dict["url"], domain=domain_id).first()
                

                if anno == None:
                    if valid_dict["group"] < 0:
                        raise ValidationError(["group"])
                    anno = Annotation(domain=domain_id, url=valid_dict["url"], group=valid_dict["group"], document=valid_dict["document"], classes=",".join(valid_dict["classes"]))
                else:
                    anno.group = valid_dict["group"]
                    anno.classes = ",".join(valid_dict["classes"])

                if anno.group > domain.groups:
                    domain.groups = anno.group
                    db.session.add(domain)

                db.session.add(anno)
                db.session.commit()
                logging.info("Created new annotation")


            except ValidationError as ve:
                return error_response(ve.message, 400)
            except Exception as e:
                logging.error(e)
                return error_response(str(e))        


        
        return jsonify(domain.to_json())
    except Exception as e:
        return error_response(str(e))

@bp.route("/<int:domain_id>/groups/<int:group_id>", methods=(["GET"]))
def show_domain_annotations_by_group(domain_id, group_id):
    try:
        if not db.session.query(Domain.query.filter_by(id=domain_id).exists()).scalar():
            return "Not found", 404

        start_index = int(request.args.get("start", default=0))
        limit = int(request.args.get("rows", 0))

        query = Annotation.query.filter_by(domain=domain_id, group=group_id).offset(start_index)

        if limit > 0:
            query = query.limit(limit)

        return jsonify([ anno.to_json() for anno in query.all() ])

            
    except Exception as e:
        logging.error(e)
        return error_response(str(e))        


@bp.route("/<int:domain_id>/groups/<int:group_id>/count", methods=(["GET"]))
def show_domain_annotations_count_by_group(domain_id, group_id):
    try:
        if not db.session.query(Domain.query.filter_by(id=domain_id).exists()).scalar():
            return "Not found", 404

        return jsonify({"count": Annotation.query.filter_by(domain=domain_id, group=group_id).count() })

            
    except Exception as e:
        logging.error(e)
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

@bp.route("/<int:domain_id>/<int:annotation_id>/document")
def show_annotation_document(domain_id, annotation_id):
    try:
        domain = Domain.query.filter_by(id=domain_id).first()
        annotation = Annotation.query.filter_by(id=annotation_id, domain=domain_id).first()

        if domain == None or annotation == None:
            return "Not found", 404

        with urllib.request.urlopen(annotation.url) as res:
            result = (str(BeautifulSoup(res.read(), "html.parser"))
                .replace('src="/', f'src="https://{ domain.name }/')
                .replace('href="/', f'href="https://{ domain.name }/')
                .replace("'/", f"'http://127.0.0.1:3000/domains/{ domain_id }/{ annotation_id }/resource?res=/"))
            return result.encode("utf-8")
    
    except Exception as e:
        return error_response(str(e))

@bp.route("/<int:domain_id>/<int:annotation_id>/resource")
def show_annotation_resource(domain_id, annotation_id):
    try:
        domain = Domain.query.filter_by(id=domain_id).first()
        annotation = Annotation.query.filter_by(id=annotation_id, domain=domain_id).first()

        if domain == None or annotation == None:
            return "Not found", 404

        # TODO: Deal with 403 errors
        with urllib.request.urlopen(f"https://{ domain.name }/{ request.args.get('res', default='') }") as res:
            return res.read()
    
    except Exception as e:
        return error_response(str(e))