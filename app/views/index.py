from flask import make_response, jsonify, request
from flask_restful import Resource, reqparse

from app.models.Models import Customers, CustomersSchema, ProductsSchema, Products
# from app.models.Products import Products, ProductsSchema
# from app.models.Categories import Categories


class HelloWorld(Resource):
    def get(self):
        return make_response(jsonify(
            {'message':'Hello World'}
        ), 200)

class Customer(Resource):
    def get(self, id):
        user_schema = CustomersSchema()
        user = Customers.get_by_id(id)
        result = user_schema.dump(user)
        return result
    

class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        
        user_schema = CustomersSchema()
        customer = Customers(
            first_name = json_data['first_name'],
            last_name = json_data['last_name'],
            email = json_data['email'],
            address = json_data['address'],
            city = json_data['city'],
            state = json_data['state'],
            zip = json_data['zip'],
            phone = json_data['phone'],
            password = json_data['password']
        )
        customer.add()
        return user_schema.dump(customer)

class Products(Resource):
    def get(self, id):
        product_schema = ProductsSchema()
        product = Products.get_by_id(id)
        result = product_schema.dump(products)
        return result


