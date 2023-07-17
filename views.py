from datetime import datetime, timedelta

from flask import render_template
from flask_smorest import Blueprint
from wtforms import StringField, IntegerField, SelectField, DecimalField
from flask_security import roles_accepted

from models import ClientModel, ItemModel, InvoiceModel
from forms import ItemForm
from db import db
from convert2pdf import print_invoice


blp = Blueprint('views', __name__, description="actions on views")

rechnungsnr = 1181

@blp.route('/')
def index():
    return render_template('index.html')

@blp.route('/neue-rechnung-erzeugen', methods=['GET','POST'])
@roles_accepted('admin')
def neue_rechnung_erzeugen():

    items = ItemModel.query.all()    
    clients = ClientModel.query.all()
    
    clients_names = []
    for client in clients:
        clients_names.append(client.name)

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
        today = datetime.now().strftime('%d.%m.%Y')
        target_date = datetime.now() + timedelta(days=10)
        target_output = target_date.strftime('%d.%m.%Y')
        global rechnungsnr
        rechnungsnr += 1
        rechnungsnummer_output = datetime.now().strftime('%Y%m') + str(rechnungsnr)
        for i in range(len(items)):
            anzahl = getattr(form, 'anzahl' + str(i+1))
            if anzahl.data > 0:
                einzelpreis = getattr(form, 'stueckpreis' + str(i+1))
                beschreibung = getattr(form, 'beschreibung' + str(i+1))
                anzahl = getattr(form, 'anzahl' + str(i+1))
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