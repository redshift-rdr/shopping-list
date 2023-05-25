import uuid, json, secrets
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date, datetime

def generate_uuid():
    return str(uuid.uuid4())

class Item(db.Model):
    """
        Model that holds the information about an actual item that is added to the shopping list
    """
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(64), index=True)
    brand = db.Column(db.String(64))
    quantity = db.Column(db.String(24))
    link = db.Column(db.Text)
    requestor = db.Column(db.String(64))
    note = db.Column(db.Text)

    def __repr__(self):
        return f'Item <{self.name}>'