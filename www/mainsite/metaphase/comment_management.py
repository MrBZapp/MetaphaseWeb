__author__ = 'BroZapp'

from metaphase import app, blogread, formread
from blogread import db as db

@app.route('/comment', methods=['GET', 'POST'])
def comment():

    post_id = app.request.args.get('post_id')

    # make sure user is logged in
    if 'user' not in app.session:
        app.flash('please log in to comment')
        return app.redirect('/log-in')
    user = app.session['user']
    user = blogread.User.query.filter_by(username=user['username']).first()
    form = formread.CommentForm()
    content = form.comment_text.data
    if app.request.method == 'POST':
        new_comment = blogread.Comment(post_id, content, user.id)
        db.session.add(new_comment)
        db.session.commit()

    commented_post = blogread.Entry.query.filter_by(id=post_id).first()
    commented_post.content = app.Markup(commented_post.content)
    comments = blogread.Comment.query.filter_by(post_id=post_id).all()

    return app.render_template('comment.html', post_id=post_id, commented_post=commented_post,
                               comments=comments, form=form, bootstrap=True)
