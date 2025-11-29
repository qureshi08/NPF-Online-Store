from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    images = db.relationship('ProductImage', backref='product', lazy='dynamic')
    variants = db.relationship('ProductVariant', backref='product', lazy='dynamic')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Product {}>'.format(self.name)

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(256))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class ProductVariant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) # e.g., "Red", "Large"
    price_modifier = db.Column(db.Float, default=0.0) # Optional: add to base price
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for guest checkout
    guest_email = db.Column(db.String(120))
    status = db.Column(db.String(20), default='Pending')
    payment_method = db.Column(db.String(50), default='Cash on Delivery')
    total_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __repr__(self):
        return '<Order {}>'.format(self.id)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price_at_purchase = db.Column(db.Float)
    product = db.relationship('Product', backref='order_items')
