from flask import render_template, request
from app.main import bp
from app.models import Product, Category

@bp.route('/')
def index():
    featured_products = Product.query.limit(4).all()
    return render_template('main/index.html', featured_products=featured_products)

@bp.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category')
    query = Product.query
    
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first_or_404()
        query = query.filter_by(category_id=category.id)
        
    products = query.paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()
    return render_template('main/shop.html', products=products, categories=categories, current_category=category_slug)

@bp.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    return render_template('main/product_detail.html', product=product)
