from flask import render_template, session, redirect, url_for, request, flash, jsonify, current_app
from app.cart import bp
from app.models import Product, Order, OrderItem
from app import db
from flask_login import current_user

@bp.route('/')
def index():
    cart = session.get('cart', {})
    products = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            total_price += product.price * quantity
            products.append({'product': product, 'quantity': quantity})
    return render_template('cart/cart.html', products=products, total_price=total_price)

@bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    session['cart'] = cart
    flash('Item added to cart.')
    return redirect(url_for('cart.index'))

@bp.route('/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    if str(product_id) in cart:
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            del cart[str(product_id)]
        session['cart'] = cart
    return redirect(url_for('cart.index'))

@bp.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
    return redirect(url_for('cart.index'))


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        if not current_user.is_authenticated and not email:
            flash('Please provide an email address.')
            return redirect(url_for('cart.checkout'))
            
        payment_method = request.form.get('payment_method', 'Cash on Delivery')
        
        order = Order(
            user_id=current_user.id if current_user.is_authenticated else None,
            guest_email=email if not current_user.is_authenticated else current_user.email,
            total_price=0,
            status='Pending',
            payment_method=payment_method
        )
        db.session.add(order)
        db.session.commit() # Commit to get ID
        
        total_price = 0
        for product_id, quantity in cart.items():
            product = Product.query.get(product_id)
            if product:
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price_at_purchase=product.price
                )
                db.session.add(item)
                total_price += product.price * quantity
                
                # Update stock
                product.stock -= quantity
                
        order.total_price = total_price
        db.session.commit()
        
        # Clear cart
        session.pop('cart', None)
        
        return redirect(url_for('cart.confirmation', order_id=order.id))
        
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            total_price += product.price * quantity
            
    return render_template('cart/checkout.html', total_price=total_price)

@bp.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('cart/confirmation.html', order=order)
