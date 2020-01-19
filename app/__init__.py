# from flask import Flask
# from flask_restful import Api
# from flask_migrate import Migrate
# from flask_marshmallow import Marshmallow
# from flask_sqlalchemy import SQLAlchemy 


# # from app.views.index import HelloWorld, Customer
# from config import config_settings

# print("app init")
# # from app.models import db

# app = Flask(__name__)
# app.config.from_object(config_settings['development'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# migrate = Migrate(app, db)
# api = Api(app)




# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(config_settings['development'])

#     api = Api(app)
#     # api.add_resource(HelloWorld, '/')
#     api.add_resource(Customer, '/api/customer/')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)
#     migrate.init_app(app, db)
#     ma = Marshmallow(app)

#     return app