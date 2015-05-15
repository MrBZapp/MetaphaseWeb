__author__ = 'BroZapp'

from flask import flash, request, session, Markup
from metaphase import app, db, blogread, formread

@app.route('/comment', methods=['GET', 'POST'])
def comment():

    post_id = request.args.get('post_id')

    # make sure user is logged in
    if 'user' not in session:
        flash('please log in to comment')
        return app.redirect('/log-in')
    user = session['user']
    user = blogread.User.query.filter_by(username=user['username']).first()
    form = formread.CommentForm()
    content = form.comment_text.data
    if app.request.method == 'POST':
        new_comment = blogread.Comment(post_id, content, user.id)
        db.session.add(new_comment)
        db.session.commit()

    commented_post = blogread.Entry.query.filter_by(id=post_id).first()
    commented_post.content = Markup(commented_post.content)
    comments = blogread.Comment.query.filter_by(post_id=post_id).all()

    return app.render_template('comment.html', post_id=post_id, commented_post=commented_post,
                               comments=comments, form=form, bootstrap=True)
