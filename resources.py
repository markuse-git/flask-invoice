from flask import jsonify
from flask_restful import Resource, Api, reqparse
from flask_smorest import Blueprint
from sqlalchemy import extract

from models import InvoiceModel


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
            # invoices = invoices.filter_by(beglichen=clear)
            invoices = invoices.filter(InvoiceModel.beglichen is True).all()
            # wenn clear= werden alle False angezeigt; wenn clear=xy alle True

        if year:
            # invoices = invoices.filter(InvoiceModel.datum.like(f'%{year}%')).all()
            invoices = invoices.filter(extract('year', InvoiceModel.datum) == year).all()  # noqa: E501

        if month:
            invoices = invoices.filter(extract('month', InvoiceModel.datum) == month).all()  # noqa: E501

        output = []

        for invoice in invoices:
            invoice_data = {}
            invoice_data['client'] = invoice.kunde
            invoice_data['datum'] = invoice.datum
            invoice_data['betrag'] = invoice.betrag

            output.append(invoice_data)

        return jsonify({'Invoices':output})
    
api.add_resource(Invoices_api, '/api/invoices')

