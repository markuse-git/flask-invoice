from fpdf import FPDF
from datetime import datetime, timedelta


rechnungsnummer = 1181

class MyInvoice(FPDF):
    def header(self):
        self.set_font("Helvetica", "",8)
        self.cell(0,5,"Peter Kuschmierz /",0,1,"L")
        self.set_font("Helvetica", "",10)

    def footer(self):
        self.set_font("Helvetica", "",8)
        text = ("Die eigene Sicherheit liegt in unseren Händen, deshalb jeißt" 
                "der gemeinsame Nenner Einschätzung und Vorhersage. Meine Firma" 
                "sagt menschliches Verhalten voraus, Verhalten in einer einzigen" 
                "Kategorie. Gewalt! Doch viel öfter sagen wir Sicherheit voraus.")
        self.write(5,text)

invoice = MyInvoice()
    
invoice.set_font("Helvetica", "", 11)

def create_item(item_args, i):
    # bei 0,1,2,3 -> 0,4,8,12 -> (+0,+1,+2,+3) -> [(0,1,2,4),(5,6,7,8),(9,10,11,12)]
    s = i * 4 
    invoice.cell(10, 10, str(i+1), 'T',0,'L',0)
    invoice.cell(60, 10, item_args[s+0], 'T',0,'L',0)
    invoice.cell(20, 10, item_args[s+1], 'T',0,'R',0)
    invoice.cell(20, 10, item_args[s+2], 'T',0,'R',0)
    invoice.cell(20, 10, item_args[s+3], 'T',0,'R',0)
    invoice.ln()

def create_pdf(item_args, client_name, brutto, strasse, plz, ort, netto, mwst):
    today_file = datetime.now().strftime('%y-%m-%d')
    today = datetime.now().strftime('%d.%m.%Y')
    target = datetime.now() + timedelta(days=14)
    target_output = target.strftime('%d.%m.%Y')
    global rechnungsnummer
    #! Loop funktioniert nicht; scheint nicht in globale var zurück zu schreiben!
    rechnungsnummer += 1 
    rechnungsnummer_output = datetime.now().strftime('%Y%m') + str(rechnungsnummer)
    
    invoice.alias_nb_pages()
    invoice.add_page()

    # LOGO
    # invoice.image('./images/logo.jpg', 160,15,40) 
    # #! verursacht z.T den Fehler KeyError: 'data'

    # Adressat
    invoice.set_font("Helvetica","",10)
    invoice.cell(0,4,client_name,0,1)
    invoice.cell(0,4,strasse,0,1)
    invoice.cell(11,4,plz,0,0)
    invoice.cell(11,4,ort,0,1)
    invoice.ln(20)

    # Base Lines
    invoice.set_font("Helvetica","B",10)
    invoice.cell(14,4,"Rg. Nr.: ",0,0)
    invoice.cell(15,4,rechnungsnummer_output,0,1)
    invoice.cell(52,4,"Rechnungs Datum: " + today,0,0)
    invoice.cell(83,4,"/ Fällig bis: " + target_output,0,1)
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
    invoice.cell(20,10, 'Menge \n/Tag(e)', 'T', 0, 'R', 1)
    invoice.cell(20,10, 'Preis', 'T', 0, 'R', 1)
    invoice.cell(20,10, 'Gesamt', 'T', 0, 'R', 1)
    invoice.ln()

    # Table Data
    invoice.set_font("Helvetica", "", 11)

    for i in range(len(item_args)//4):
        create_item(item_args, i)
        '''
        Die td werden in views in eine Liste geschrieben und diese als Parameter in die 
        Funktioncreate_pdf übergeben. Jede Zeile besteht aus 4 td. Daher wird die 
        Funktion create_item sooft aufgerufen, wie es Zeilen gibt (len(item_args)/4). 
        // damit daraus kein float wird, sondern ein int bleibt. i wird in create_item 
        als parameter mitgegeben, damit der startpunkt (s) für den index geändert 
        werden kann. Damit bei jedem Aufrufe der Funktion ein anderes item 
        generiert wird.
        '''

    invoice.cell(90,10, 'Summe Netto:', 'T', 0, 'R', 0)
    invoice.cell(40,10, netto, 'T', 1, 'R', 0)
    invoice.cell(90,10, 'gesetzl. MwSt.:', 'T', 0, 'R', 0)
    invoice.cell(40,10, mwst, 'T', 1, 'R', 0)
    invoice.set_text_color(255,255,255)
    invoice.set_fill_color(36,84,101)
    invoice.cell(90,10, 'Summe Brutto:', 'T', 0, 'R', 1)
    invoice.cell(40,10, brutto, 'T', 1, 'R', 1)
    
    invoice.ln(10)

    invoice.set_text_color(0,0,0)

    # Zahlungshinweis
    invoice.set_font("Helvetica", "", 10)
    hinweis = ("Überweisen Sie bitte die Rechnungssumme innerhalb von 10 Tagen" 
               "auf das rechts genannte Bankkonto.")
    # invoice.write(5,hinweis)
    invoice.multi_cell(130,5,hinweis,0)
    invoice.ln(20)

    # Unterschriftszeile
    invoice.set_font("Helvetica", "", 11)
    invoice.cell(100,10, today, 0,0,"L",0)
    invoice.ln()
    invoice.cell(90,10,"Ort, Datum",'T',0,"L",0)
    invoice.cell(40,10,"Peter Kuschmierz",'T',0,"R",0)

    invoice.ln(15)

    # Sidebar
    sidebar = ("Postadresse:\n"
                 "P / Kuschmierz\n"
                 "Organisationsberatung\n"
                 "Ruhrtalstr.33a (Tor3)\n"
                 "45239 Essen\n"
                 "\n"
                 "////////////////////////\n"
                 "\n"
                 "Kontakt:\n"
                 "Tel.: 0201 / 451 387 00\n"
                 "Mobil: 0172 / 454 4 167\n"
                 "info@pkuschmierz.de\n"
                 "www.pkuschmierz.de\n"
                 "\n"
                 "////////////////////////\n"
                 "\n"
                 )
    
    invoice.multi_cell(58,5, sidebar, 0)

    invoice.ln(20)
 
    path = "./reports/" + client_name.replace(' ','').lower() + "_" + today_file + ".pdf"  # noqa: E501
    invoice.output(path)