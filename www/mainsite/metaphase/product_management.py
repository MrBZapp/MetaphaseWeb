__author__ = 'BroZapp'
import copy
from flask import redirect, request, render_template, session
from metaphase import app,  blogDB


@app.route('/order')
def order():
    # get the right product from the database
    pid = request.args.get('product')
    product = blogDB.Product.query.filter_by(id=pid).first()

    # if there are products left available
    if product.qty >= 1:
        add_to_cart(product)
    return redirect('projects')

# send me an e-mail there's been an order

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart = assemble_cart_from_session()
    base = app.jinja_env.get_template('cart.html')
    return render_template(base, title="Cart", cart=cart)


###########################################################


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
        session['cart_cost'] += product.real_price() * session_cart()[p]

    return session['cart_cost']