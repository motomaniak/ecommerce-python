from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate


from app.views.index import HelloWorld, Customer
from config import config_settings
from app.models import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_settings['development'])

    api = Api(app)
    api.add_resource(HelloWorld, '/')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app