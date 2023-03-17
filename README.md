# App zur Erzeugung und Suche von Rechnungen
  
- Positionssummen
- Rechnungssumme
- MwSt

- Form zum Suchen von Rechnugnen, API?

## offene Fragen

platzhalter

## Plan

- pdf wird erzeugt
- es wird ein Datensatz in der Tabelle 'Rechnungen' erzeugt. Inkl. pdf (Nr., Datum, Kunde, Betrag, beglichen?, pdf)
- Nach Rechnungs-Suche wird die Summe der Rechnungsbeträge ausgegeben
- Rechnungssuche nach Datum (Jahr, Monat), Kunde, beglichen?

## Fixes

- In der Tabelle items_invoices werden keine Einträge gesetzt
- manchmal wird eine neue DB unter instance erzeugt; manchemal im Hauptverzeichnis

## Modifikationen

- Neue Rechnung erzeugen -> Feld 'Zur Rechnung?' wird eigentlich nicht benötigt. Hinzugefügt wird wenn Anzahl > 0
- Das Feld 'Zur Rechnung' muss entsprechend nicht in das ItemModel; dann auch nicht unter Admin/Item
- Das Feld 'Anzahl' wird in der DB (Items) eigentlich nicht benötigt
