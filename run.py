# from app import create_app
# from app.models import db
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy 

from config import config_settings

app = Flask(__name__)
app.config.from_object(config_settings['development'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)

from app.views.index import HelloWorld, Categories, OrderDetails, Customer, Register, Product, Products, Login, AddProdcutToOrder, Order

api.add_resource(HelloWorld, '/')
api.add_resource(Customer, '/api/customer/<int:id>')
api.add_resource(Register, '/api/register')
api.add_resource(Products, '/api/products')
api.add_resource(Product, '/api/product/<int:id>')
api.add_resource(Login, '/api/login')
api.add_resource(AddProdcutToOrder, '/api/order/add')
api.add_resource(Order, '/api/order/<int:id>')
api.add_resource(Categories, '/api/categories')

if __name__ == '__main__':
    app.run(debug=True)