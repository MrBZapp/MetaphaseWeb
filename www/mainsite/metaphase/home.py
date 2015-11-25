__author__ = 'BroZapp'

from flask import render_template, redirect, Markup
from metaphase import app
import metaphase.blogDB as blogread
from sqlalchemy import exc as sql_exception

@app.route('/home')
def home():
    try:
        # get all the 'orphan' entries
        entries = blogread.Post.query.filter_by(parent_id=None).all()

    except sql_exception.OperationalError:
        user = blogread.User("Server", "Server", "Server", "Not Your Business")
        entries = [blogread.Post(user=user, content="The server forgot to provide any data or something,\
            we're not positive yet. <br> Give it a shot again but please cool it contact the system administrator \
            if the problem persists.", title="Whoops")]

    if entries is not None:
        for entry in entries:
            entry.content = Markup(entry.content)

        # may those that are last, be first.
        entries.reverse()

    return render_template('base.html', title="home", posts=entries, bootstrap=True)


#CATCH ALL
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect('home')