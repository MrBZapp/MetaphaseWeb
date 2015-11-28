__author__ = 'BroZapp'
import copy
from flask import redirect, request, render_template, session, url_for
from metaphase import app,  blogDB

shipping_options = [
    {
        'name': 'Slow',
        'price': 500
    },
    {
        'name': 'Fast',
        'price': 1500
    }]


@app.route('/order')
def order():
    # get the right product from the database
    pid = request.args.get('product')
    product = blogDB.Product.query.filter_by(id=pid).first()

    # if there are products left available
    if product.qty >= 1:
        add_to_cart(product)
    return redirect('projects')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    action = request.args.get('action')
    args = request.args
    if action == 'Update Cart':
        update_cart()

    if action == 'Empty Cart':
        session['cart'] = {}

    if action == 'Checkout':
        update_cart()
        session['Shipping'] = request.args.get('Shipping')
        return redirect('checkout')

    total_cart_items()
    total_cart_cost()
    kart = assemble_cart_from_session()
    base = app.jinja_env.get_template('cart.html')
    return render_template(base, title="Cart", cart=kart, shipping_options=shipping_options)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'Shipping' in session:
        kart = assemble_cart_from_session()
        shipping = session['Shipping']

        cart_sum = total_cart_cost()
        total = cart_sum + shipping

        base = app.jinja_env.get_template('checkout.html')
        return render_template(base, title="Checkout", cart=kart, total=total)
    else:
        return redirect('/cart')


###########################################################
def update_cart():
    for item in request.args:
        if item in session['cart']:
            session['cart'][item] = int(request.args.get(item))

def session_cart():
    if 'cart' not in session.keys():
        session['cart'] = {}
    return session['cart']


def add_to_cart(product, qty=1):
    kart = session_cart()
    if str(product.id) in kart:
        kart[str(product.id)] += qty
        total_cart_items()
        total_cart_cost()
        return
    kart[product.id] = qty
    total_cart_items()
    total_cart_cost()


def assemble_cart_from_session():
    kart = []
    for p in session_cart():
        warehouse_product = blogDB.Product.query.filter_by(id=p).first()
        cart_product = copy.copy(warehouse_product)
        cart_product.qty = session_cart()[p]
        kart.append(cart_product)
    return kart


def total_cart_items():
    session['cart_count'] = sum(session_cart().itervalues())
    return session['cart_count']


def total_cart_cost():
    session['cart_cost'] = 0.00
    for p in session_cart():
        product = blogDB.Product.query.filter_by(id=p).first()
        session['cart_cost'] += product.price * session_cart()[p]

    return session['cart_cost']