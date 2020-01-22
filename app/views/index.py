from flask import make_response, jsonify, request
from flask_restful import Resource
from werkzeug.security import check_password_hash

from app.models.Models import Customers, CustomersSchema, ProductsSchema, Products, OrderDetails
from app.models import Models


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

    def put(self, id):
        customer_schema = CustomersSchema()
        json_data = request.get_json(force=True)
        customer = Models.Customers.update(id, json_data)
        result = customer_schema.dump(customer)
        return result
    

class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        
        user_schema = CustomersSchema()
        customer = Customers(
            first_name = NULL,
            last_name = NULL,
            email = json_data['email'],
            address = NULL,
            city = NULL,
            state = NULL,
            zip = NULL,
            phone = NULL,
            password = json_data['password']
        )
        customer.add()
        return user_schema.dump(customer)

class Login(Resource):
    def get(self):
        json_data = request.get_json(force=True)
        customer_schema = CustomersSchema()
        customer = Models.Customers.get_by_email(json_data)
        customer_model = customer_schema.dump(customer)
        valid_password = check_password_hash(customer_model['password'], json_data['password'])
        
        if(valid_password):
            return customer_model
        else:
            return jsonify({'msg':'Password or email is incorrect'})

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

class OrderDetails(Resource):
    def get(self, id):
        order_details = Models.OrderDetails.get(id)
        for order in order_details:
            print(order[0])
        return jsonify({"result":"I hate my life"})
        
class Order(Resource):
    def get(self, id):
        order_schema = Models.OrdersSchema(many=True)
        order = Models.OrderDetails.get(id)
        print(order)
        result = Models.OrderDetailsSchema(many=True).dump(order)
        # print(result[0].order_date)
        return result