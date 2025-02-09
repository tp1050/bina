from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Brand(db.Model):
    __tablename__ = 'brands'
    brand_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', backref='brand', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    internal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    gtin = db.Column(db.String(14), nullable=False, unique=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.brand_id'))
    brand_name = db.Column(db.String(100))
    image_src = db.Column(db.String(2048))
    images = db.relationship('Image', secondary='product_images', order_by='ProductImage.display_order')

class Image(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(2048), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    product_id = db.Column(db.Integer, db.ForeignKey('products.internal_id'), primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), primary_key=True)
    display_order = db.Column(db.Integer, default=0)
# from flask import Flask
# from models import db

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/products1'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# # Example query to get products with their images ordered by display_order
# @app.route('/products')
# def get_products():
#     products = Product.query.all()
#     return [{'name': p.name, 'images': [{'url': img.url} for img in p.images]} for p in products]
