# App zur Erzeugung und Suche von Rechnungen

Rechnungen werden über etf Fromular erfasst, als html erzeugt, als pdf gespeichert und in der DB (sqlite) gespeichert. Per Admin können Kunden, Leistungen und Rechnungen verwaltet werden. Über API werden die Rechnungen abgefragt und mit Betragssummen ausgegeben.

## Packages

migrate, restful, security, smorest, sqlalchemy, WTF, pdfkit, admin, sass

## Besonderheiten

- DB n:m Beziehung (Invoice, Item)
- Berechnung von Betragssummen
- CSS animiertes Menü
- Komplexe Abfrage für RESTFul API
- Anpassung von Security Templates
- Condition User Authentifizierung in jinja2
- Design (Rechnung)

## Schwierigkeiten

- n:m Beziehung -> Daten in Connection Table schreiben
- API RESTful -> komplexe Abfrage gestalten
- Fortlaufende Rechnungsnummer
- Layout der 2 spaltigen Rechnung + Speicherung ans pdf
