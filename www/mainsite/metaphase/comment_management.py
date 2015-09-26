__author__ = 'BroZapp'

from flask import request, Markup, render_template
from metaphase import app, db, blogDB, user_management, formread

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    parent = blogDB.Post.query.filter_by(id=request.args.get('post_id')).first()
    form = formread.CommentForm(request.form)

    if request.method == 'POST':
        user_management.verify_user_log_in()
        user = user_management.session_user()
        new_comment = blogDB.Post(user, form.comment_text.data, parent=parent, title='comment')
        db.session.add(new_comment)
        db.session.commit()

    commented_post = blogDB.Post.query.filter_by(id=parent.id).first()
    commented_post.content = Markup(commented_post.content)
    comments = blogDB.Post.query.filter_by(parent_id=parent.id).all()

    return render_template('comment.html', post=parent, comments=comments, form=form, bootstrap=True)
