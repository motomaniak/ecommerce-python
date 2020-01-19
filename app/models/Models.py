from run import db, ma
from datetime import datetime

class Categories(db.Model):
    __tablename__ ='categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # products = db.relationship('Products', backref='categories', lazy=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Category {}>'.format(self.name)


    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def get_all(self):
        pass

class CategoriesSchema(ma.ModelSchema):
    class Meta:
        model = Categories

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    description = db.Column(db.Text)
    image = db.Column(db.String())
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Categories', foreign_keys=category_id)

    def __init__(self, name, description, image, quantity, price, category_id):
        self.name = name,
        self.description = description,
        self.image = image,
        self.quantity = quantity,
        self.price = price,
        self.category_id = category_id

    def __repr__(self):
        return '<Product {}>'.format(self.name)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def get_all(self):
        pass

    def get_by_id(self, id):
        return Products.query.filter_by(id=id).one()


class ProductsSchema(ma.ModelSchema):
    class Meta:
        model = Products
        

from run import db, ma
from werkzeug.security import generate_password_hash

class Customers(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))
    email = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255))
    city = db.Column(db.String(50))
    state = db.Column(db.String(10))
    zip = db.Column(db.String(20))
    phone = db.Column(db.String(30))
    password = db.Column(db.String(200))

    def __init__(self, first_name, last_name, email, address, city, state, zip, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<Customer {}>'.format(self.first_name + " " + self.last_name)

    def get_by_id(id):
        return Customers.query.filter_by(id=id).one()
    
    def add(self):
        print(self.first_name)
        db.session.add(self)
        db.session.commit()
        return self

class CustomersSchema(ma.ModelSchema):
    class Meta:
        model = Customers


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    order_date = db.Column(db.DateTime)
    shippid_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customers', foreign_keys=customer_id)
    order_details = db.relationship('OrderDetails', cascade='all,delete', backref='Orders')

    def __init__(self, customer_id):
        self.status = "Pending"
        self.customer_id = customer_id
        self.shippid_date = NULL 

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, id):
        order = Orders.query.filter_by(id=id).one()
        db.session.delete(order)
        db.commit()

class OrdersSchema(ma.ModelSchema):
    class meta:
        model = Orders

class OrderDetails(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey(Products.id), primary_key=True)
    order_id = db.Column(db.Integer,  db.ForeignKey(Orders.id), primary_key=True)
    quantity = db.Column(db.Integer)
    list_price = db.Column(db.Float)
    discount = db.Column(db.Float, db.CheckConstraint('0<=discount<1'))

    def __init__(self, product_id, order_id, quantity, list_price, discount):
        self.product_id = product_id
        self.order_id = order_id
        self.quantity = quantity
        self.list_price = list_price
        self.discount = discount

    def add(self):
        db.session.add(self)
        db.commit()
        return self

    def delete(self, id):
        pass

class OrderDetailsSchema(ma.ModelSchema):
    class meta:
        model = OrderDetails


    


    

