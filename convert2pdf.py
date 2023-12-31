import pdfkit


# --------- PDFKIT -----------------

def print_invoice(html_path, pdf_path):
    options = {
        'page-size':'Letter',
        'margin-top':'0.45in',
        'margin-right':'0.75in',
        'margin-bottom':'0.75in',
        'margin-left':'0.75in',
        'encoding':'UTF-8',
        'no-outline':None,
        'enable-local-file-access':None
    }

    css = "./static/css/style.css"

    pdfkit.from_string(html_path, pdf_path, options=options, css=css)