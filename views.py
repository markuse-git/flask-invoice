from datetime import datetime

from flask import render_template, redirect, url_for
from flask_smorest import Blueprint
from wtforms import StringField, BooleanField, IntegerField, FloatField, SelectField

from models import ClientModel, ItemModel, InvoiceModel
from forms import ItemForm
from db import db
from report import create_pdf

blp = Blueprint('views', __name__, description="actions on views")


@blp.route('/')
def index():
    return 'das steht schon mal'

@blp.route('/neue-rechnung-erzeugen', methods=['GET','POST'])
def neue_rechnung_erzeugen():

    items = ItemModel.query.all()    
    clients = ClientModel.query.all()
    
    clients_names = []
    for client in clients:
        clients_names.append(client.name)

    ItemForm.client = SelectField('client', choices=clients_names)

    for item in items:
        setattr(ItemForm, 'beschreibung' + str(item.id), StringField(item.beschreibung))
        setattr(ItemForm, 'stueckpreis' + str(item.id), FloatField(item.stueckpreis))
        setattr(ItemForm, 'anzahl' + str(item.id), IntegerField(item.anzahl, default=0))
        setattr(ItemForm, 'zur_rechnung' + str(item.id), BooleanField(item.zur_rechnung, default=False))

    form = ItemForm()

    output = ''
    if form.validate_on_submit():
        results = {}
        item_args = []
        for i in range(len(items)):
            rechnung = getattr(form, 'zur_rechnung' + str(i+1))
            if rechnung.data == True:
                einzelpreis = getattr(form, 'stueckpreis' + str(i+1))
                beschreibung = getattr(form, 'beschreibung' + str(i+1))
                anzahl = getattr(form, 'anzahl' + str(i+1))
                result = float(einzelpreis.data) * float(anzahl.data)
                results[i] = result
                item_args.append(beschreibung.data)
                item_args.append(str(anzahl.data))
                item_args.append(str(einzelpreis.data))
                item_args.append(str(result))
            final_result = 0
            for r in results:
                final_result = final_result + results[r]
            brutto = final_result * 1.19
            mwst = final_result * 0.19

        # um unter kunde die client.id speichern zu können; Sonst wird Client nicht unter Admin/Invoice angezeigt
        client = ClientModel.query.filter(ClientModel.name == form.client.data).first()

        client_name = client.name
        strasse = client.strasse
        plz = client.plz
        ort = client.ort

        new_invoice = InvoiceModel(
            datum = datetime.now(),
            betrag = brutto,
            beglichen = False,
            kunde = client.id
        )
        db.session.add(new_invoice)
        db.session.commit()

        create_pdf(
            item_args,
            brutto=str(brutto), 
            client_name=client_name,
            strasse = strasse,
            plz = str(plz),
            ort = ort,
            netto = str(final_result),
            mwst = str(mwst)
        )
        
            
        output = "Rechnung wurde erzeugt"

    return render_template('neue-rechnung.html', form=form, items=items, clients=clients, output=output)