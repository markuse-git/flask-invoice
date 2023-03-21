from fpdf import FPDF
from datetime import datetime, timedelta

class MyInvoice(FPDF):
    def header(self):
        
        self.set_font("Helvetica", "",8)
        self.cell(0,5,"Peter Kuschmierz /",0,1,"L")
        self.set_font("Helvetica", "",10)
        
def create_pdf(client_name, brutto, str, plz, ort):
    today_file = datetime.now().strftime('%y-%m-%d')
    today = datetime.now().strftime('%d.%m.%Y')
    target = datetime.now() + timedelta(days=14)
    target_output = target.strftime('%d.%m.%Y')

    invoice = MyInvoice()
    invoice.alias_nb_pages()
    invoice.add_page()

    # Adressat
    invoice.set_font("Helvetica","",10)
    invoice.cell(0,4,client_name,0,1)
    invoice.cell(0,4,str,0,1)
    invoice.cell(11,4,plz,0,0)
    invoice.cell(11,4,ort,0,1)
    invoice.ln(20)

    # Base Lines
    invoice.cell(14,4,"Rg. Nr.: ",0,0)
    invoice.cell(15,4,"2022101181",0,1)
    invoice.cell(49,4,"Rechnungs Datum: " + today,0,0)
    invoice.cell(49,4,"/ Fällig bis: " + target_output,0,1)
    invoice.cell(49,4,"Fälliger Betrag: " + brutto + " Euro",0,1)
    invoice.ln(10)

    # Tabelle
    invoice.set_font("Helvetica", "B", 11)
    invoice.set_line_width(0.4)
    invoice.set_draw_color(192,192,192)
    invoice.set_fill_color(255,255,255)
    invoice.set_text_color(0,0,0)

    # Table Head
    invoice.cell(10,10, 'Nr', 'T', 0, 'L', 1)
    invoice.cell(60,10, 'Beschreibung', 'T', 0, 'L', 1)
    invoice.cell(30,10, 'Menge /' + '\n' + 'Tag(e)', 'T', 0, 'R', 1)
    invoice.cell(30,10, 'Preis', 'T', 0, 'R', 1)
    invoice.cell(30,10, 'Gesamt', 'T', 0, 'R', 1)
    invoice.ln()

    # Table Data
    invoice.set_font("Helvetica", "", 11)
    invoice.cell(10,10, '1', 'T', 0, 'L', 1)
    invoice.cell(60,10, 'Das ist eine Position', 'T', 0, 'L', 1)
    invoice.cell(30,10, '2,00', 'T', 0, 'R', 1)
    invoice.cell(30,10, '1.000,00', 'T', 0, 'R', 1)
    invoice.cell(30,10, '2.000,00', 'T', 0, 'R', 1)
    invoice.ln()



    invoice.output("./reports/" + client_name.replace(' ','').lower() + "_" + today_file + ".pdf")