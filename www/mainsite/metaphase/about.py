__author__ = 'BroZapp'

from flask import render_template
from metaphase import app

@app.route('/about')
def about():
    return render_template('about.html', title="home", bootstrap=True)