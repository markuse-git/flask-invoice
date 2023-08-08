from flask import jsonify
from flask_restful import Resource, Api, reqparse
from flask_smorest import Blueprint
from sqlalchemy import extract

from models import InvoiceModel, ClientModel


blp = Blueprint('resources', __name__, description="actions on resources")

api = Api(blp)

class Invoices_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client', type=int, help='Client ID')
        parser.add_argument('year', type=int, help='Year')
        parser.add_argument('month', type=str, help='Month')
        parser.add_argument('clear', type=bool, help='Cleared?')

        args = parser.parse_args()
        client_id = args.get('client')
        year = args.get('year')
        month = args.get('month')
        clear = args.get('clear')

        invoices = InvoiceModel.query

        if client_id:
            invoices = invoices.filter_by(kunde=client_id)

        if clear:
            invoices = invoices.filter(InvoiceModel.beglichen == 1)
            # wenn clear= werden alle False angezeigt; wenn clear=xy alle True

        if year:
            invoices = invoices.filter(extract('year', InvoiceModel.datum) == year)

        if month:
            invoices = invoices.filter(extract('month', InvoiceModel.datum) == month)
            
        results = invoices.all()
        '''
        durch .all() wird das query object zu einer Liste. Auf diese kann dann 'filter '
        nicht mehr angewendet werden. 
        '''
        
        output = []

        for invoice in results:
            # Um statt IDs Namen auszugeben
            kunde = ClientModel.query.filter_by(id=invoice.kunde).first()

            invoice_data = {}
            invoice_data['client'] = kunde.name
            invoice_data['datum'] = invoice.datum.strftime('%Y %b')
            invoice_data['betrag'] = invoice.betrag
            invoice_data['cleared'] = invoice.beglichen

            output.append(invoice_data)

        return jsonify({'Invoices':output})
    
api.add_resource(Invoices_api, '/api/invoices')

