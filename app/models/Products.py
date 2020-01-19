from run import db, ma

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
        

