from flask import make_response, jsonify, request, abort
from flask_restful import Resource
from werkzeug.security import check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app.models.Models import Customers, CustomersSchema, ProductsSchema, Products, OrderDetails
from app.models import Models
from run import jwt

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401

class Customer(Resource):
    @jwt_required
    def get(self, id):
        user_schema = CustomersSchema()
        customer_id = get_jwt_identity()
        user = Customers.get_by_id(customer_id)
        result = user_schema.dump(user)
        return {'customer': result}
    
    @jwt_required
    def put(self, id):
        customer_schema = CustomersSchema()
        customer_id = get_jwt_identity()
        json_data = request.get_json(force=True)
        customer = Models.Customers.update(customer_id, json_data)
        result = customer_schema.dump(customer)
        return result
    

class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        user_schema = CustomersSchema()
        customer = Customers(
            first_name = None,
            last_name = None,
            email = json_data['email'],
            address = None,
            city = None,
            state = None,
            zip = None,
            phone = None,
            password = json_data['password']
        )
        try:
            customer.add()
            access_token = create_access_token(identity = customer.id)
            refresh_token = create_refresh_token(identity = customer.id)
            return {'customer': user_schema.dump(customer), 'access_token': access_token, 'refresh_token': refresh_token }
        except:
            return {'msg': 'Something went wrong'}, 500

class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        customer_schema = CustomersSchema()
        customer = Models.Customers.get_by_email(json_data)
        customer_model = customer_schema.dump(customer)
        valid_password = check_password_hash(customer_model['password'], json_data['password'])
        
        if(valid_password):
            access_token = create_access_token(identity=customer.id)
            refresh_token = create_refresh_token(identity=customer.id)
            return {'customer': customer_model, 'access_token': access_token, 'refresh_token': refresh_token}
        else:
            return {'error':'Password or email is incorrect'}, 401

class Product(Resource):
    def get(self, id):
        product_schema = ProductsSchema()
        product = Models.Products.get_by_id(id)
        result = product_schema.dump(product)
        return result

    def post(self):
        json_data = request.get_json(force=True)
        product_schema = ProductsSchema()
        product = Models.Products(
            name = json_data['name'],
            description = json_data['description'],
            image = json_data['image'],
            quantity = json_data['quantity'],
            price = json_data['price'],
            category_id = json_data['category_id']
        )
        product.add()
        return product_schema.dump(product)

    def put(self, id):
        product_schema = ProductsSchema()
        json_data = request.get_json(force=True)
        product = Models.Products.update(id, json_data)
        result = product_schema.dump(product)
        return result
        

class Products(Resource):
    def get(self):
        product_schema = ProductsSchema(many=True)
        products = Models.Products.get_all()
        result = product_schema.dump(products)
        return result

class Categories(Resource):
    def get(self):
        categories = Models.Categories.get_all()
        results = Models.CategoriesSchema(many=True).dump(categories)
        return results

class AddProdcutToOrder(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        model = Models.OrderDetails.add(json_data)
        return model
        
class Order(Resource):
    def get(self, id):
        order_schema = Models.OrdersSchema(many=True)
        order = Models.OrderDetails.get(id)
        result = Models.OrderDetailsSchema(many=True).dump(order)
        return result

class Orders(Resource):
    def get(self, id):
        order_schema = Models.OrdersSchema(many=True)
        orders = Models.Orders.get(id)
        result = order_schema.dump(orders)
        return result

class Cart(Resource):
    def get(self):
        customer_id = get_jwt_identity()
        cart_shema = Models.CartSchema()
        cart = Models.Orders.get_cart(customer_id)
        result = cart_shema.dump(cart)
        return result

    def delete(self):
        json_data = request.get_json(force=True)
        result = Models.OrderDetails.delete(json_data['product_id'], json_data['order_id'])
        return result

    def put(self):
        json_data = request.get_json(force=True)
        result = Models.OrderDetails.update(json_data['order_id'], json_data['product_id'], int(json_data['quantity']))
        return result


class Checkout(Resource):
    def put(self):
        json_data = request.get_json(force=True)
        result = Models.Orders.checkout(json_data['order_id'])
        return result 
