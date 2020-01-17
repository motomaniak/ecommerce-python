from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from app.models.Customers import Customers

class HelloWorld(Resource):
    def get(self):
        return make_response(jsonify(
            {'message':'Hello World'}
        ), 200)


