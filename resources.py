from flask import jsonify
from flask_restful import Resource, Api
from flask_smorest import Blueprint

from models import InvoiceModel


blp = Blueprint('resources', __name__, description="actions on resources")

api = Api(blp)

class Invoices_api(Resource):
    def get(self, client):
        invoices = InvoiceModel.query.all()

        if invoices:
            output = []
            results = [invoice for invoice in invoices if invoice.kunde == int(client)]

            for invoice in results:
                invoice_data = {}
                invoice_data['client'] = invoice.kunde
                invoice_data['datum'] = invoice.datum
                invoice_data['betrag'] = invoice.betrag

                output.append(invoice_data)

        return jsonify({'Invoices':output})
    
api.add_resource(Invoices_api, '/api/invoices/<client>')

