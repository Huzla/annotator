from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Domain(db.Model):
    __tablename__ = "domains"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    index_page = db.Column(db.String())
    groups = db.Column(db.Integer)
    annotations = db.relationship("Annotation", backref="domains", lazy=True, cascade="all, delete")
    
    db.UniqueConstraint(name, index_page)

    def __init__(self, name, index_page, groups=0):    
        self.name = name
        self.index_page = index_page
        self.groups = groups

    def __repr__(self):
        return f"<Domain { self.name } with { self.groups } groups>"

    def to_json(self, exclude=[]):
        keys = ["id", "name", "index_page", "groups"]

        result = { key: getattr(self, key) for key in keys if key not in exclude }
        
        return result


class Annotation(db.Model):
    __tablename__ = "annotations"

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Integer, db.ForeignKey("domains.id"))
    url = db.Column(db.String())
    document = db.Column(db.Unicode())
    group = db.Column(db.Integer)
    classes = db.Column(db.String())

    db.UniqueConstraint(domain, url)

    def __init__(self, domain, url, document, group, classes):
        self.domain = domain.id if isinstance(domain, Domain) else domain
        self.url = url
        self.group = group
        self.document = document
        self.classes = classes

    def __repr__(self):
        return f"<Annotation at { self.url } of group { self.group } >"

    def to_json(self, exclude=[]):
        keys = ["id", "url", "group", "classes", "domain", "document"]

        json_form = { 
            "id": self.id,
            "url": self.url,
            "group": self.group,
            "classes": self.classes.split(","),
            "document": self.document,
            "domain": self.domain
        }

        return { key: json_form[key] for key in keys if key not in exclude }
