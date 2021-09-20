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

    def __init__(self, name, index_page, groups=0, id=None):
        if id != None:
            self.id = id
            
        self.name = name
        self.index_page = index_page
        self.groups = groups

    def __repr__(self):
        return f"<Domain { self.name } with { self.groups } groups>"

    def to_json(self):
        return { 
            "id": self.id,
            "name": self.name,
            "index_page": self.index_page,
            "groups": self.groups,
         }


class Annotation(db.Model):
    __tablename__ = "annotations"

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Integer, db.ForeignKey("domains.id"))
    url = db.Column(db.String())
    group = db.Column(db.Integer)
    classes = db.Column(db.String())

    db.UniqueConstraint(domain, url)

    def __init__(self, domain, url, group, classes, id=None):
        if id != None:
            self.id = id
        
        self.domain = domain.id
        self.url = url
        self.group = group
        self.classes = classes

    def __repr__(self):
        return f"<Annotation at { self.url } of group { self.group } >"

    def to_json():
        return {
            "id": self.id,
            "url": self.url,
            "group": self.group,
            "classes": self.classes.split(","),
            "domain": self.domain
        }
