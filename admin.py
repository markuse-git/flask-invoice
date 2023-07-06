from flask_admin.contrib.sqla import ModelView

class ClientView(ModelView):
    form_excluded_columns = ['invoices']

class ItemView(ModelView):
    form_excluded_columns = ['invoice']
    column_exclude_list = ['anzahl']

class InvoiceView(ModelView):
    form_excluded_columns = ['items']