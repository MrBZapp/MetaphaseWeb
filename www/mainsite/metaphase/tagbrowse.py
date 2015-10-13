__author__ = 'BroZapp'

from flask import request, render_template, redirect, flash
from metaphase import app, blogDB

@app.route('/tags')
def tags():
    tag = blogDB.Tag.query.filter_by(id=request.args.get('tag_id')).first()
    if tag is not None:
        posts = tag.posts
        base = app.jinja_env.get_template('tags.html')
        title = "Items tagged as: "+tag.value
        return render_template(base, title=title, tag=tag, posts=posts, bootstrap=True)
    else:
        flash('invalid tag ID')
        return redirect('home')

