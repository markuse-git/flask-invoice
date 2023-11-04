from db import db
from flask_login import UserMixin


# Client:Invoice => 1:n
# Invoice:Item => n:m

class ClientModel(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    strasse = db.Column(db.String(100))
    plz = db.Column(db.Integer)
    ort = db.Column(db.String(100))

    invoices = db.relationship('InvoiceModel', backref='client', lazy='dynamic')

    def __repr__(self) -> str:
        return self.name
    
class Items_Invoices(db.Model):
    __tablename__ = 'items_invoices'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    
class InvoiceModel(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.DateTime)
    betrag = db.Column(db.Numeric(7,2))    
    nr = db.Column(db.Integer)
    offen = db.Column(db.String(25))

    kunde = db.Column(db.Integer, db.ForeignKey('client.id'))

    items = db.relationship('ItemModel', secondary='items_invoices', backref='invoice')  # noqa: E501

    def __repr__(self) -> str:
        return self.id
        
class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    beschreibung = db.Column(db.Text(200))
    stueckpreis = db.Column(db.Numeric(7,2))

    # invoices = db.relationship('InvoiceModel', secondary='items_invoices', backref='item', lazy='dynamic')  # noqa: E501

    def __repr__(self) -> str:
        return self.id

# FLASK SECURITY

class Roles_Users(db.Model):
    __tablename__ = 'roles_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    descsription = db.Column(db.String(255))

    def __repr__(self) -> str:
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    fs_uniquifier = db.Column(db.String(64))

    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))  # noqa: E501

