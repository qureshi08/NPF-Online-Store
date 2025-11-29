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
    search_query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'newest')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    
    query = Product.query
    
    # Filter by Category
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first_or_404()
        query = query.filter_by(category_id=category.id)
        
    # Filter by Search Query
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
        
    # Filter by Price
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    # Sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name_asc':
        query = query.order_by(Product.name.asc())
    else: # newest
        query = query.order_by(Product.created_at.desc())
        
    products = query.paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()
    
    return render_template('main/shop.html', 
                         products=products, 
                         categories=categories, 
                         current_category=category_slug,
                         search_query=search_query,
                         sort_by=sort_by,
                         min_price=min_price,
                         max_price=max_price)

@bp.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    return render_template('main/product_detail.html', product=product)
