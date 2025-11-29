from flask import render_template, flash, redirect, url_for, request
from app import db
from app.admin import bp
from app.admin.forms import CategoryForm, ProductForm
from app.models import Category, Product
from flask_login import login_required, current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/base.html')

@bp.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@bp.route('/category/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, slug=form.name.data.lower().replace(' ', '-'))
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully.')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='New Category')

@bp.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = form.name.data.lower().replace(' ', '-')
        db.session.commit()
        flash('Category updated successfully.')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='Edit Category')

@bp.route('/category/delete/<int:id>')
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted.')
    return redirect(url_for('admin.categories'))

@bp.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@bp.route('/product/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_product():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            slug=form.name.data.lower().replace(' ', '-'),
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data
        )
        db.session.add(product)
        db.session.commit()
        
        if form.image.data:
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(form.image.data)
            from app.models import ProductImage
            image = ProductImage(image_url=upload_result['secure_url'], product_id=product.id)
            db.session.add(image)
            db.session.commit()
            
        flash('Product created successfully.')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', form=form, title='New Product')

@bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        product.name = form.name.data
        product.slug = form.name.data.lower().replace(' ', '-')
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        db.session.commit()

        if form.image.data:
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(form.image.data)
            from app.models import ProductImage
            # For MVP, just add new image. Could delete old ones or manage multiple.
            image = ProductImage(image_url=upload_result['secure_url'], product_id=product.id)
            db.session.add(image)
            db.session.commit()

        flash('Product updated successfully.')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', form=form, title='Edit Product')

@bp.route('/product/delete/<int:id>')
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.')
    return redirect(url_for('admin.products'))

@bp.route('/orders')
@login_required
@admin_required
def orders():
    from app.models import Order
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@bp.route('/order/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(id):
    from app.models import Order
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status:
        order.status = new_status
        db.session.commit()
        flash(f'Order {order.id} status updated to {new_status}.')
    return redirect(url_for('admin.orders'))
