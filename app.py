from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin

from views import blp as ViewsBlueprint
from resources import blp as ResourcesBlueprint
from admin import ClientView, InvoiceView, ItemView, RolesView, UserView
from models import ClientModel, InvoiceModel, ItemModel, Role, User  # noqa: E501

import logging

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
    admin.add_view(ClientView(ClientModel, db.session, 'Clients'))
    admin.add_view(ItemView(ItemModel, db.session, 'Items'))
    admin.add_view(InvoiceView(InvoiceModel, db.session, 'Invoices'))
    admin.add_view(RolesView(Role, db.session, 'Roles'))
    admin.add_view(UserView(User, db.session, 'Users'))


    app.register_blueprint(ViewsBlueprint)
    app.register_blueprint(ResourcesBlueprint) # API registrieren

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate()
    migrate.init_app(app, db)

    logging.basicConfig(level=logging.DEBUG)
    
    return app


