from flask import render_template, redirect, url_for
from flask_smorest import Blueprint

from models import ClientModel, ItemModel, InvoiceModel
from forms import ItemForm


blp = Blueprint('views', __name__, description="actions on views")

@blp.route('/')
def index():
    return 'das steht schon mal'

@blp.route('/neue-rechnung-erzeugen')
def neue_rechnung_erzeugen():
    items = ItemModel.query.all()    
    clients = ClientModel.query.all()
    form = ItemForm()

    return render_template('neue-rechnung.html', form=form, items=items, clients=clients)