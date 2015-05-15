__author__ = 'BroZapp'

from metaphase import app
from metaphase.blogread import db

db.create_all()
app.run(debug=True)