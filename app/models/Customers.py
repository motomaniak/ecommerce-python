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

