from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    gtin = db.Column(db.String(14), unique=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    brand = db.Column(db.String(255))
    company = db.Column(db.String(255))
    source = db.Column(db.String(255))

class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.Numeric(10,2))
    date = db.Column(db.Date)
    seller_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

# Additional model classes for Person, Inventory, Invoice etc.
