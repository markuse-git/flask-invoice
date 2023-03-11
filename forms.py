from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField

from models import ItemModel


class ItemForm(FlaskForm):
    items = ItemModel.query.all()
    for item in items:
        beschreibung = StringField('Beschreibung', default=item.beschreibung)
        stueckpreis = StringField('Stueckpreis', default=item.stueckpreis)
        anzahl = IntegerField('Anzahl', default=0)
        zur_rechnung = BooleanField('Zur_Rechnung', default=False)