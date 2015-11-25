__author__ = 'BroZapp'

from flask import redirect, request
from metaphase import app,  blogDB


@app.route('/order')
def order():
    # get the right product from the database
    pid = request.args.get('product')
    product = blogDB.Product.query.filter_by(id=pid).first()

    # if there are products left available
    if product.qty >= 1:
        #add product to cart
        product.qty -= 1

    return redirect('projects')

# send me an e-mail there's been an order
