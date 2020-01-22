from run import db, ma
from werkzeug.security import generate_password_hash
from flask import jsonify


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    description = db.Column(db.Text)
    image = db.Column(db.String())
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    # category = db.relationship('Categories', foreign_keys=category_id)
    order_details = db.relationship('OrderDetails', backref='prodcuts', lazy=True)

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
    
    def get_all():
        return db.session.query(Products).all()
        # return Products.query.join(Categories).all()
        # return Products.query.options(joinedload('categories')).all()[0].categories

    def get_by_id(id):
        return Products.query.filter_by(id=id).join(Categories).one()

    def update(id, json_data):
        product = Products.query.filter_by(id=id).first()
        product.name = json_data['name']
        product.description = json_data['description']
        product.quantity = json_data['quantity']
        product.image = json_data['image']
        product.category_id = json_data['category_id']

        db.session.commit()


class Categories(db.Model):
    __tablename__ ='categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    products = db.relationship('Products', backref='categories', lazy=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Category {}>'.format(self.name)


    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def get_all():
        return Categories.query.all()


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
        db.session.add(self)
        db.session.commit()
        return self

    def update(id, json_data):
        customer = Customers.query.filter_by(id=id).first()
        customer.first_name = json_data['first_name']
        customer.last_name = json_data['last_name']
        customer.email = json_data['email']
        customer.address = json_data['address']
        customer.city = json_data['city']
        customer.state = json_data['state']
        customer.zip = json_data['zip']
        customer.phone = json_data['phone']
        customer.password = generate_password_hash(json_data['password'])
        db.session.commit()

    def get_by_email(json_data):
        customer = Customers.query.filter_by(email=json_data['email']).first()
        return customer


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    order_date = db.Column(db.DateTime)
    shippid_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customers', foreign_keys=customer_id)
    order_details = db.relationship('OrderDetails', cascade='all,delete', backref='orders')

    def __init__(self, customer_id):
        self.status = "Pending"
        self.customer_id = customer_id
        self.shippid_date = None 

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, id):
        order = Models.Orders.query.filter_by(id=id).one()
        db.session.delete(order)
        db.session.commit()

    def get(id):
        order = Orders.query.filter_by(customer_id=id).all()
        return order
        

    def __repr__(self):
        return '<Order {}>'.format(self.id)


class OrderDetails(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey(Products.id), primary_key=True)
    order_id = db.Column(db.Integer,  db.ForeignKey(Orders.id), primary_key=True)
    quantity = db.Column(db.Integer)
    list_price = db.Column(db.Float)
    discount = db.Column(db.Float, db.CheckConstraint('0<=discount<1'))
    product = db.relationship('Products', backref='orderdetails')
    order = db.relationship('Orders', backref='orderdetails')

    def __init__(self, product_id, order_id, quantity, list_price, discount):
        self.product_id = product_id
        self.order_id = order_id
        self.quantity = quantity
        self.list_price = list_price
        self.discount = discount

    def add(json_data):
        order_id = None
        order = Orders.query.filter_by(customer_id=json_data['customer_id'], status='Pending').first()
        if not order:
            new_order = Orders(json_data['customer_id'])
            db.session.add(new_order)
            db.session.commit()
            order_id = new_order.id
        else:
            order_id = order.id
        product = Products.query.filter_by(id=json_data['product_id']).with_for_update().one()
        if product.quantity < json_data['quantity']:
            return jsonify({'msg':'Error, not enough items'})
        else:  
            product.quantity -= json_data['quantity']
            db.session.commit()
            order_details = OrderDetails(json_data['product_id'], order_id, json_data['quantity'], product.price, json_data['discount'])
            db.session.add(order_details)
            db.session.commit()
            return jsonify({"msg":"OK", "status":200})

    def get(id):
        order_details = OrderDetails.query.filter_by(order_id=id)
        return order_details

    def delete(self, id):
        pass

class CustomersSchema(ma.ModelSchema):
    class Meta:
        model = Customers
    
class CategoriesSchema(ma.ModelSchema):
    class Meta:
        model = Categories
        fields = ['name'] 

class ProductsSchema(ma.ModelSchema):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'quantity', 'image', 'category']
    category = ma.Nested(CategoriesSchema)

class OrderDetailsSchema(ma.ModelSchema):
    class Meta:
        model = OrderDetails
        fields = ['order_id', 'quantity', 'list_price', 'discount', 'product']
    product = ma.Nested(ProductsSchema)

class OrdersSchema(ma.ModelSchema):
    class Meta:
        model = Orders
        fields = ['id', 'order_date', 'shipped_date', 'status', 'order_details']
    order_details = ma.Nested(OrderDetailsSchema, many=True)

