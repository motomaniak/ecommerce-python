from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS 
from flask_jwt_extended import JWTManager

from config import config_settings

app = Flask(__name__)
app.config.from_object(config_settings['development'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['JWT_SECRET_KEY'] = 'rW27%NkfVQMUq%hnj%9RCp&9s$pkpfqVNwbbuwn'
ma = Marshmallow(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
CORS(app)

api = Api(app)

from app.views.index import Orders, Categories, OrderDetails, Customer, Register, Product, Products, Login, AddProdcutToOrder, Order

api.add_resource(Customer, '/api/customer/<int:id>')
api.add_resource(Register, '/api/auth/register')
api.add_resource(Products, '/api/products')
api.add_resource(Product, '/api/product/<int:id>')
api.add_resource(Login, '/api/auth/login')
api.add_resource(AddProdcutToOrder, '/api/order/add')
api.add_resource(Order, '/api/order/<int:id>')
api.add_resource(Orders, '/api/orders/<int:id>')
api.add_resource(Categories, '/api/categories')

if __name__ == '__main__':
    app.run(debug=True)