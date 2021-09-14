from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Domain(db.Model):
    __tablename__ = "domains"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    index_page = db.Column(db.String())
    groups = db.Column(db.Integer)
    annotations = db.relationship("Annotation", backref="domain", lazy=True, cascade="all, delete")

    def __init__(self, name, index_page, groups):
        self.name = name
        self.index_page = index_page
        self.groups = groups

    def __repr__(self):
        return f"<Domain { self.name } with { self.groups } groups>"


class Annotation(db.Model):
    __tablename__ = "annotation"

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Integer, db.ForeignKey("domain.id"))
    url = db.Column(db.String())
    group = db.Column(db.Integer)
    classes = db.Column(db.String())

    def __init__(self, domain, url, group, classes):
        self.domain = domain
        self.url = url
        self.group = group
        self.classes = classes

    def __repr__(self):
        return f"<Annotation at { self.url } of group { self.group } >"
