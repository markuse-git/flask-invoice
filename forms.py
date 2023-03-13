from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField


class ItemForm(FlaskForm):
    beschreibung = StringField('Beschreibung')
    stueckpreis = StringField('Stueckpreis')
    anzahl = IntegerField('Anzahl', default=0)
    zur_rechnung = BooleanField('Zur_Rechnung', default=False)