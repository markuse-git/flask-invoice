from flask_admin.contrib.sqla import ModelView


# um die Datum Anzeige in Admin/Invoices zu verändern
# view, context wird benötigt, damit die Anzeige auf Admin/Invoices funktioniert
def date_formatter(view, context, model, name): 
    datetime_value = getattr(model, name)
    return datetime_value.strftime('%Y-%m-%d')

class ClientView(ModelView):
    form_excluded_columns = ['invoices']
    
class ItemView(ModelView):
    form_excluded_columns = ['invoice']

class InvoiceView(ModelView):
    # column_hide_backrefs = False # Discord antwort
    # form_columns = ["kunde", "datum", "betrag", "beglichen", "items"] # Discord antwort  # noqa: E501
    #! Discort Lines führen zu Fehler bei admin/invoicemodel 
    #! TypeError: __str__ returned non-string (type int)
    form_excluded_columns = ['items']
    form_choices = {
        'offen' : [
            ('ja','ja'),
            ('nein','nein')
        ]
    }

    # Um die Anzeige in Admin/Invoices zu verändern. 
    column_formatters = {
        'datum': date_formatter
    }

class RolesView(ModelView):
    pass

class UserView(ModelView):
    column_list = ('email', 'active', 'roles')

