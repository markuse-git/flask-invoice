from flask import render_template, redirect, url_for
from flask_smorest import Blueprint
from wtforms import StringField, BooleanField, IntegerField, FloatField

from models import ClientModel, ItemModel, InvoiceModel
from forms import ItemForm


blp = Blueprint('views', __name__, description="actions on views")

@blp.route('/')
def index():
    return 'das steht schon mal'

@blp.route('/neue-rechnung-erzeugen', methods=['GET','POST'])
def neue_rechnung_erzeugen():

    items = ItemModel.query.all()    
    clients = ClientModel.query.all()

    for item in items:
        setattr(ItemForm, 'beschreibung', StringField(item.beschreibung))
        setattr(ItemForm, 'stueckpreis', FloatField(item.stueckpreis))
        setattr(ItemForm, 'anzahl', IntegerField(item.anzahl, default=0))
        setattr(ItemForm, 'zur_rechnung', BooleanField(item.zur_rechnung, default=False))

    form = ItemForm()

    return render_template('neue-rechnung.html', form=form, items=items, clients=clients)