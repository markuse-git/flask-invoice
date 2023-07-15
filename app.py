from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_security import Security

from views import blp as ViewsBlueprint
from admin import ClientView, InvoiceView, ItemView
from models import ClientModel, InvoiceModel, ItemModel, user_datastore

from db import db


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '123123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_PASSWORD_SALT'] = 'mysalt'
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    app.config['SECURITY_RECOVERABLE'] = True
    app.config['SECURITY_CHANGEABLE'] = True

    admin = Admin(app, template_mode='bootstrap3')
    # admin = Admin(app, base_template='/templates/admin/master.html')
    admin.add_view(ClientView(ClientModel, db.session))
    admin.add_view(ItemView(ItemModel, db.session))
    admin.add_view(InvoiceView(InvoiceModel, db.session))

    Security(app, user_datastore)

    app.register_blueprint(ViewsBlueprint)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate()
    migrate.init_app(app, db)
    
    return app


