from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Domain(db.Model):
    __tablename__ = "domains"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    index_page = db.Column(db.String())
    groups = db.Column(db.Integer)

    def __init__(self, name, index_page, groups):
        self.name = name
        self.index_page = index_page
        self.groups = groups

    def __repr__(self):
        return f"<Domain { self.name } with { self.groups } groups>"