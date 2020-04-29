from run import db, ma
from werkzeug.security import generate_password_hash
from flask import jsonify
from sqlalchemy import func
from flask_marshmallow import fields
import simplejson

class Categories(db.Model):
    __tablename__ ='categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # products = db.relationship('Products', backref='categories')

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

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    description = db.Column(db.Text)
    image = db.Column(db.String())
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Categories')
    images = db.relationship('ProductImages')

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
        # return db.session.query(Products).all()
        result = Products.query.all()
        # q = db.session.query(Products.id, Products.name, Products.description, Products.image, Products.quantity, Products.category_id, func.avg(Reviews.rating).label('avg_rating')).outerjoin(Reviews, Products.id == Reviews.product_id).group_by(Products.id, Products.name, Products.price, Products.quantity, Products.category_id, Products.description, Products.image).all()
        # print(q)
        return result
    
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

class ProductImages(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_location = db.Column(db.String())
    product = db.relationship('Products', backref='productimages')

    

    def __init__(self, product_id, image_location):
        self.product_id = product_id
        self.image_location = image_location

    def __repr__(self):
        return '<ProductImage {}>'.format(self.image_location)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def get_by_prodcut_id(product_id):
        return ProductImages.query.filter_by(product_id=product_id).all()

    def update(self):
        pass

    def delete(id):
        image = ProductImages.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(image)
            db.session.commit()
            return {"message":"OK"}, 200
        except e: 
            return {"error": e}, 500

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
        customer = Customers.query.filter_by(id=id).first_or_404()
        customer.first_name = json_data['first_name']
        customer.last_name = json_data['last_name']
        customer.email = json_data['email']
        customer.address = json_data['address']
        customer.city = json_data['city']
        customer.state = json_data['state']
        customer.zip = json_data['zip']
        customer.phone = json_data['phone']
        # customer.password = generate_password_hash(json_data['password'])
        db.session.commit()
        return customer

    def get_by_email(json_data):
        customer = Customers.query.filter_by(email=json_data['email']).first_or_404()
        return customer

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    order_date = db.Column(db.DateTime)
    shipped_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    # customer = db.relationship('Customers', foreign_keys=customer_id)
    order_details = db.relationship('OrderDetails', cascade='all,delete', backref='orders')

    def __init__(self, customer_id, order_date):
        self.status = "Pending"
        self.customer_id = customer_id
        self.shipped_date = None 
        self.order_date = order_date

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, id):
        order = Models.Orders.query.filter_by(id=id).one()
        db.session.delete(order)
        db.session.commit()

    def get(id):
        order = Orders.query.filter_by(customer_id=id).filter(Orders.status != "Pending").all()
        return order

    def get_cart(id):
        order = Orders.query.filter_by(customer_id=id).filter(Orders.status == "Pending").first()
        return order

    def checkout(id):
        order = Orders.query.filter_by(id=id).first_or_404()
        order.status = "Paid"
        try:
            db.session.commit()
            return {"message":"OK"}, 200
        except e: 
            return {"error": e}, 500
        

    def __repr__(self):
        return '<Order {}>'.format(self.id)

class OrderDetails(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey(Products.id), primary_key=True)
    order_id = db.Column(db.Integer,  db.ForeignKey(Orders.id), primary_key=True)
    quantity = db.Column(db.Integer)
    list_price = db.Column(db.Float)
    discount = db.Column(db.Float, db.CheckConstraint('0<=discount<1'))
    product = db.relationship('Products', backref='orderdetails')
    # order = db.relationship('Orders', backref='orderdetails')

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
            new_order = Orders(json_data['customer_id'], json_data['date'])
            db.session.add(new_order)
            db.session.commit()
            order_id = new_order.id
        else:
            order_id = order.id
        product = Products.query.filter_by(id=json_data['product_id']).with_for_update().one()
        if product.quantity < json_data['quantity']:
            return {'error':'Error, not enough items in inventory'}, 500
        else:  
            product.quantity -= json_data['quantity']
            db.session.commit()
            order_details = OrderDetails(json_data['product_id'], order_id, json_data['quantity'], product.price, json_data['discount'])
            try:
                db.session.add(order_details)
                db.session.commit()
                return {"message":"OK"}, 200
            except Exception as e:
                return {"error": e}, 500

    def get(id):
        order_details = OrderDetails.query.filter_by(order_id=id)
        return order_details

    def delete(product_id, order_id):
        item = OrderDetails.query.filter_by(product_id=product_id).filter_by(order_id=order_id).first_or_404()
        product = Products.query.filter_by(id=product_id).first_or_404()
        product.quantity += item.quantity
        try:
            db.session.delete(item)
            db.session.commit()
            count = OrderDetails.query.filter_by(order_id=order_id).count()
            if count == 0:
                order = Orders.query.filter_by(id=order_id).first()
                try:
                    db.session.delete(order)
                    db.session.commit()
                    return {"message": "OK"}, 200
                except Exception as e:
                    return {"error": e}, 500
            return {"message":"OK"}, 200 
        except Exception as e:
            return {"error": e}, 500
    
    def update(order_id, product_id, quantity):
        item = OrderDetails.query.filter_by(product_id=product_id).filter_by(order_id=order_id).first_or_404()
        product = Products.query.filter_by(id=product_id).first_or_404()
        if product.quantity < quantity - item.quantity:
            return {'error':'Error, not enough items in inventory'}, 500
        if item.quantity > quantity:
            put_items_back = item.quantity - quantity
            product.quantity += put_items_back
        else:
            take_out_items = quantity - item.quantity
            product.quantity -= take_out_items
        item.quantity = quantity
        try:
            db.session.commit()
            return {"message": "OK"}, 200
        except Exception as e:
            return {"error": e}, 500

class Reviews(db.Model):
    __tablename__ = 'reviews'

    product_id = db.Column(db.Integer, db.ForeignKey(Products.id), primary_key=True)
    customer_id = db.Column(db.Integer,  db.ForeignKey(Customers.id), primary_key=True)
    rating = db.Column(db.Integer, db.CheckConstraint('rating <= 5 and rating >= 1'))
    review = db.Column(db.String)

    def __init__(self, product_id, customer_id, rating, review):
        self.product_id = product_id
        self.customer_id = customer_id
        self.rating = rating
        self.review = review

    def __repr__(self):
        return '<Review {}>'.format(self.review)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {"message":"OK"}, 200
        except e:
            return {"error": e}, 500
    
    def get_reviews_by_product(product_id):
        # avg = db.session.query(func.avg(Reviews.rating).label('avg_rating')).filter_by(product_id=product_id).all()
        return Reviews.query.filter_by(product_id=product_id).all()

    def get_avg_rating(product_id):
        return db.session.query(func.avg(Reviews.rating).label('avg_rating')).filter_by(product_id=product_id).all()

class ReviewsSchema(ma.ModelSchema):
    class Meta:
        model = Reviews
        fields = ['rating', 'review', 'customer_id']

class CustomersSchema(ma.ModelSchema):
    class Meta:
        model = Customers
    
class CategoriesSchema(ma.ModelSchema):
    class Meta:
        model = Categories
        fields = ['name'] 

class ProductImagesSchema(ma.ModelSchema):
    class Meta:
        model = ProductImages
        fields = ['image_location']

class ProductsSchema(ma.ModelSchema):
    # avg_rating = ma.Float()
    class Meta:
        # json_module = simplejson
        model = Products
        fields = ('id', 'name', 'description', 'quantity', 'image', 'category', 'price', 'images', 'avg_rating')
    category = ma.Nested(CategoriesSchema)
    images = ma.Nested(ProductImagesSchema, many=True)

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

class CartSchema(ma.ModelSchema):
    class Meta:
        model = Orders
        fields = ['id', 'order_date', 'shipped_date', 'status', 'order_details']
    order_details = ma.Nested(OrderDetailsSchema, many=True)

