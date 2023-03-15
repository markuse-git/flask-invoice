from db import db

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
    
class InvoiceModel(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Date)
    betrag = db.Column(db.Numeric)    
    beglichen = db.Column(db.Boolean)

    kunde = db.Column(db.Integer, db.ForeignKey('client.id'))

    items = db.relationship('ItemModel', secondary='items_invoices', backref='invoice')

    def __repr__(self) -> str:
        return self.id
        
class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    beschreibung = db.Column(db.Text(200))
    stueckpreis = db.Column(db.Float)
    anzahl = db.Column(db.Numeric)
    zur_rechnung = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return self.id

db.Table(
    'items_invoices',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('invoice_id', db.Integer, db.ForeignKey('invoice.id'))
)

