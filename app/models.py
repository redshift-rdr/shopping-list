from app import db
from datetime import datetime

class ShoppingListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    recurring = db.Column(db.Boolean, default=False)
    
    slist_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'))
    slist = db.relationship('ShoppingList', back_populates='items')

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Date, default=datetime.utcnow)
    archived = db.Column(db.Boolean, default=False)

    items = db.relationship('ShoppingListItem', back_populates='slist')