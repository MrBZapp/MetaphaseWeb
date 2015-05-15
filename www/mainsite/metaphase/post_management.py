__author__ = 'BroZapp'

from flask import flash, redirect, render_template, request, session
from metaphase import app, db, formread, blogread
from _file_helpers import allowed_file
from sqlalchemy import exc as sql_exception
from metaphase.user_management import verify_user_log_in, verify_user_admin
import werkzeug
import os

@app.route('/post', methods=['GET', 'POST'])
def post():
    # make sure user is logged in
    verify_user_log_in()

    # if the user is trying to post, make sure they have the credentials.
    if verify_user_admin():
        form = formread.BlogForm(request.form)

        # if we're submitting the form as opposed to requesting it do these things.
        if request.method == 'POST':

            # import the form content
            if 'bodyHTML' not in request.files or form.textHTML.data != "":
                content = form.textHTML.data

            # if the form is empty, upload the file, the effect is identical.
            else:
                bodyHTML = request.files['bodyHTML']
                content = bodyHTML.read()

            # prepare to import the uploaded image file
            filename = None

            # get header image
            if 'headIMG' in request.files:
                headIMG = request.files['headIMG']

                # if the file is legit replace the filename with it
                if headIMG and allowed_file(headIMG.filename):
                    filename = werkzeug.secure_filename(headIMG.filename)
                    headIMG.save(os.path.join(app.root_path, app.config['POST_IMG_FOLDER'], filename))
                    flash('file submitted')
                else:
                    flash('If a file was submitted it was of a non-allowed format.')

            # add the entry to the database
            entry = blogread.Entry(author=session['user']['realname'], title=form.title.data, content=content, imgpath=filename)
            try:
                db.session.add(entry)
                db.session.commit()
                return redirect('/')
            except sql_exception.OperationalError:
                flash('Post was not able to be submitted due to a server error.  Maybe try again?')

        base = app.jinja_env.get_template('makepost.html')
        return render_template(base, title="entering post", form=form, bootstrap=True)
    else:
        return redirect('log-in')


@app.route('/edit-post', methods=['GET', 'POST'])
def edit_post():
    # make sure user is logged in
    verify_user_log_in()

    if verify_user_admin():
        # pull the entry from the database
        try:
            entry = blogread.Entry.query.filter_by(id=request.args.get('entry')).first()
        except sql_exception.OperationalError:
            entry = blogread.Entry("General Error", "Whoops", "The server had a senior moment, or something like that.\
              Give it a minute and try again, and then contact the administrator", "")

        # if the entry doesn't exist, tell the user.
        if entry is None:
            flash("There are no posts with ID # " + request.args.get('entry') + " to be edited.")
            return redirect('/')

        form = formread.BlogForm(request.form)

        # update the relevant parts of the post
        if request.method == 'POST':
            if form.textHTML.data != "":
                entry.content = form.textHTML.data
                flash("content updated")

            if form.title.data != "":
                entry.title = form.title.data
                flash("title updated")

            # get header image
            if 'headIMG' in request.files:
                headIMG = request.files['headIMG']

                # if the file is legit replace the filename with it
                if headIMG and allowed_file(headIMG.filename):
                    filename = werkzeug.secure_filename(headIMG.filename)
                    headIMG.save(os.path.join(app.root_path, app.config['POST_IMG_FOLDER'], filename))

                    # update the entry
                    entry.headIMG = filename
                    flash("head image updated")

            db.session.commit()

            return redirect('/')

        else:
            # pre-populate the form:
            form = formread.BlogForm(title=entry.title, textHTML=entry.content)

        base = app.jinja_env.get_template('edit-post.html')
        return render_template(base, title="editing post", form=form, id=request.args.get('entry'), bootstrap=True)

    else:
        return redirect('log_in')

