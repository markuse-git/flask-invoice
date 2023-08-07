import requests
from requests.exceptions import RequestException
import json

from datetime import datetime, timedelta

from flask import render_template
from flask_smorest import Blueprint
from wtforms import StringField, IntegerField, SelectField, DecimalField, BooleanField
from flask_security import roles_accepted
from sqlalchemy import desc

from models import ClientModel, ItemModel, InvoiceModel, Items_Invoices
from forms import ItemForm, InvoicesForm
from db import db
from convert2pdf import print_invoice


blp = Blueprint('views', __name__, description="actions on views")


def get_client_names():
    clients = ClientModel.query.all()
        
    clients_names = []
    for client in clients:
        clients_names.append(client.name)

    return clients_names

def get_invoices_dates():
    invoices = InvoiceModel.query.all()

    invoices_dates = []
    for invoice in invoices:
        if invoice.datum.year not in invoices_dates:
            invoices_dates.append(invoice.datum.year)

    return invoices_dates

@blp.route('/')
def index():
    return render_template('index.html')

@blp.route('/neue-rechnung-erzeugen', methods=['GET','POST'])
@roles_accepted('admin')
def neue_rechnung_erzeugen():

    items = ItemModel.query.all()    
    clients = ClientModel.query.all()
    
    clients_names = get_client_names()

    ItemForm.client = SelectField('client', choices=clients_names)

    for item in items:
        setattr(ItemForm, 'beschreibung' + str(item.id), StringField(item.beschreibung))
        setattr(ItemForm, 'stueckpreis' + str(item.id), DecimalField(item.stueckpreis))
        setattr(ItemForm, 'anzahl' + str(item.id), IntegerField(item.anzahl, default=0))

    form = ItemForm()

    output = ''
    if form.validate_on_submit():
        results = {}
        item_args = []

        item_ids = [] # weil der db Eintrag erst gemacht werden kann, wenn es einen Eintrag für die Invoice ID gibt  # noqa: E501

        today = datetime.now().strftime('%d.%m.%Y')
        target_date = datetime.now() + timedelta(days=10)
        target_output = target_date.strftime('%d.%m.%Y')
        
        # um die Rechnungsnummer auf dem pdf fortlaufend zu machen
        invoices = InvoiceModel.query.order_by(desc(InvoiceModel.datum)).first()
        if invoices:
            last_invoice_id = invoices.id
        else:
            last_invoice_id = 0

        new_invoice_id = last_invoice_id + 1182 # um bei 1182 anzufangen
        rechnungsnummer_output = datetime.now().strftime('%Y%m') + str(new_invoice_id)
        
        for i in range(len(items)):
            anzahl = getattr(form, 'anzahl' + str(i+1))
            if anzahl.data > 0:
                einzelpreis = getattr(form, 'stueckpreis' + str(i+1))
                beschreibung = getattr(form, 'beschreibung' + str(i+1))
                anzahl = getattr(form, 'anzahl' + str(i+1))

                # items_invoices: aktuelle ID des Items suchen
                item_id = ItemModel.query.filter(ItemModel.beschreibung == beschreibung.data).first()  # noqa: E501
                if item_id:
                    item_ids.append(item_id.id)

                result = float(einzelpreis.data) * float(anzahl.data)
                results[i] = result 
                item_args.append(beschreibung.data)
                item_args.append(str(anzahl.data))
                item_args.append(str(einzelpreis.data))
                item_args.append('{:.2f}'.format(result)) #todo data type anpassen
            final_result = 0
            for r in results:
                final_result = final_result + results[r] 
            brutto = '{:.2f}'.format(final_result * 1.19) #todo data type anpassen
            mwst = '{:.2f}'.format(final_result * 0.19)  #todo data type anpassen
            netto = '{:.2f}'.format(final_result)

        # um unter kunde die client.id speichern zu können; Sonst wird Client nicht unter Admin/Invoice angezeigt  # noqa: E501
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

        # die ID der soeben gespeicherten Invoice suchen
        invoice_id = InvoiceModel.query.order_by(desc(InvoiceModel.datum)).first()

        # für jedes Item einen eigenen Eintrag in der association table machen
        for item_id in item_ids:
            new_items_invoices = Items_Invoices(
                item_id = item_id,
                invoice_id = invoice_id.id
            )
            db.session.add(new_items_invoices)
            db.session.commit()

        #* Vorläufig zugunsten der html Rechnung deaktiviert
        # create_pdf(
        #     item_args,
        #     brutto=str(brutto), 
        #     client_name=client_name,
        #     strasse = strasse,
        #     plz = str(plz),
        #     ort = ort,
        #     netto = str(final_result),
        #     mwst = str(mwst)
        # )
            
        output = "Rechnung wurde erzeugt"

        # todo statt return rendered =
        rendered = render_template(
            'invoice-float.html', 
            item_args=item_args,
            client_name=client_name,
            strasse=strasse,
            plz=str(plz),
            ort=ort,
            netto=str(netto),
            mwst=str(mwst),
            brutto=str(brutto),
            today=today,
            target_output=target_output,
            rechnungsnummer_output=rechnungsnummer_output
            )
        
        # todo zu reaktivieren!
        today_file = datetime.now().strftime('%y-%m-%d')
        pdf_repo = "./reports/" + client_name.replace(' ','').lower() + "_" + rechnungsnummer_output  + "_" + today_file + ".pdf"  # noqa: E501
        print_invoice(rendered, pdf_repo)
        
    return render_template('neue-rechnung.html', form=form, items=items, clients=clients, output=output)  # noqa: E501


@blp.route('/invoices', methods=['GET','POST'])
def invoices():

    clients_names = get_client_names()
    clients_names.append('All')
    invoices_dates = get_invoices_dates()
    invoices_dates.append('All')
    months = ['All', 'Jan', 'Feb', 'Mrz', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']  # noqa: E501
    
    InvoicesForm.client = SelectField('Client', choices=clients_names, default='All')
    InvoicesForm.year = SelectField('Year', choices=invoices_dates, default='All')
    InvoicesForm.month = SelectField('Month', choices=months, default='All')
    InvoicesForm.cleared = BooleanField('Cleared')

    form = InvoicesForm()

    months = {
            'Jan':1,
            'Feb':2,
            'Mrz':3,
            'Apr':4,
            'Mai':5,
            'Jun':6,
            'Jul':7,
            'Aug':8,
            'Sep':9,
            'Okt':10,
            'Nov':11,
            'Dez':12,
        }

    qstrg = {}

    if form.validate_on_submit():

        if form.client.data != 'All':
            client = ClientModel.query.filter_by(name=form.client.data).first()
            qstrg['client'] = client.id
        if form.year.data != 'All':
            qstrg['year'] = form.year.data
        if form.month.data != 'All':
            qstrg['month'] = months[form.month.data]
        if form.cleared.data is True:
            qstrg['clear'] = form.cleared.data

        try:
            json_data = json.dumps(qstrg)
            url = 'http://127.0.0.1:5000/api/invoices?'
            headers = {'Content-Type':'application/json'}
            response = requests.get(url, data=json_data, headers=headers)
            data = response.json()
        except RequestException as e:
            print(f"Request Exception: {e}")
            response = {'result':None}
        except json.decoder.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            response = {'result':None}

        invoice_data = data if data else []
        
    # print(url)

    return render_template('invoices.html', form=form, invoice_data=invoice_data)