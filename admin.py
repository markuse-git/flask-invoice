from flask_admin.contrib.sqla import ModelView

class ClientView(ModelView):
    form_excluded_columns = ['invoices']
    
class ItemView(ModelView):
    form_excluded_columns = ['invoice']
    column_exclude_list = ['anzahl']

class InvoiceView(ModelView):
    # column_hide_backrefs = False # Discord antwort
    # form_columns = ["kunde", "datum", "betrag", "beglichen", "items"] # Discord antwort  # noqa: E501
    #! Discort Lines führen zu Fehler bei admin/invoicemodel 
    #! TypeError: __str__ returned non-string (type int)
    form_excluded_columns = ['items']

class RolesView(ModelView):
    pass
