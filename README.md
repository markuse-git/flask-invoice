# App zur Erzeugung und Suche von Rechnungen
  
- Positionssummen
- Rechnungssumme
- MwSt

- Form zum Suchen von Rechnugnen, API?

## offene Fragen

- wenn einzelene Positionen in der DB gespeichert werden
  - wie können in der Tabellenausgabe 'Anzahl' und 'zur Rechnung hinzufügen' nachträglich gesetzt werden?

## Plan

- In der Tabellenansicht der Positionen können 'Anzahl' und 'zur Rechnung hinzufügen' upgedated werden
- Unter Tabellenansicht (Positionen): Rechnung für Kunde (select) + Btn Rechnung erzeugen
- pdf wird erzeugt
- es wird ein Datensatz in der Tabelle 'Rechnungen' erzeugt. Inkl. pdf (Nr., Datum, Kunde, Betrag, beglichen?, pdf)
- Nach Rechnungs-Suche wird die Summe der Rechnungsbeträge ausgegeben
- Rechnungssuche nach Datum (Jahr, Monat), Kunde, beglichen?

## Aufbau

- Neue Rechnung erzeugen Seite mit Ausgabe Tabelle Items
  - Statt einer Abfrage sollte das wohl eher ein Formular (wtf) mit vobelegten Werten aus der Abfrage sein
  - wenn das Formular abgeschickt wird ...
    - Update der Items (Anzahl, Zur_Rechnung)
    - Erzeugen der pdf rechnung
    - Uodate der Items (Anzahl, Zur_Rechnung) -> NULL
