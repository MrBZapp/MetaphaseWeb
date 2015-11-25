__author__ = 'BroZapp'

from flask import flash, redirect, render_template, request, session
from metaphase import app, db, formread, blogDB
from _file_helpers import allowed_file
from sqlalchemy import exc as sql_exception
from metaphase.user_management import verify_user_log_in, verify_user_admin
import werkzeug, os, string as s, csv

@app.route('/post', methods=['GET', 'POST'])
def post():
    # make sure user is logged in
    verify_user_log_in()

    # if the user is trying to post, make sure they have the credentials.
    verify_user_admin()
    form = formread.BlogForm(request.form)
    projects = blogDB.Project.query.all()
    form.projects.choices = [(project.id, project.title) for project in projects]


    # if we're submitting the form as opposed to requesting it do these things.
    if request.method == 'POST':

        # import the form content
        if 'bodyHTML' not in request.files or form.textHTML.data != "":
            content = form.textHTML.data

        # if the form is empty, upload the file, the effect is identical.
        else:
            bodyHTML = request.files['bodyHTML']
            content = bodyHTML.read()

        # get header image
        if 'headIMG' in request.files:
            headIMG = request.files['headIMG']

            # if the file is legit replace the filename with it
            if headIMG and allowed_file(headIMG.filename):
                file_name = werkzeug.secure_filename(headIMG.filename)
                headIMG.save(os.path.join(app.root_path, app.config['POST_IMG_FOLDER'], file_name))
                flash('file submitted. ')
            else:
                flash('If a file was submitted it was of a non-allowed format.')
        user = blogDB.User.query.filter_by(username=session['user']['username']).first()

        entry = blogDB.Post(user=user, title=form.title.data, content=content)

        for tags in csv.reader(form.tags.data.split('\n'), delimiter=','):
            for tag in tags:
                new_tag = blogDB.Tag(tag.lstrip().rstrip().lower())
                old_tag = blogDB.Tag.query.filter_by(value=new_tag.value).first()
                if old_tag is None:
                    entry.tags.append(new_tag)
                else:
                    entry.tags.append(old_tag)

        # attach the projects
        form_projects = form.projects.data
        projects = blogDB.Project.query.filter(blogDB.Project.id.in_(form_projects)).all()

        # add the entry to the database
        try:

            db.session.add(entry)
            db.session.commit()

            for project in projects:
                project.rel_posts.append(entry)

            db.session.commit()

            return redirect('/home')
        except sql_exception.OperationalError:
            flash('Post was not able to be submitted due to a server error.  Maybe try again?')

    base = app.jinja_env.get_template('makepost.html')
    return render_template(base, title="entering post", form=form, bootstrap=True)


@app.route('/edit-post', methods=['GET', 'POST'])
def edit_post():
    # make sure user is logged in and is an administrator
    verify_user_log_in()
    verify_user_admin()

    # pull the entry from the database
    try:
        entry = blogDB.Post.query.filter_by(id=request.args.get('entry')).first()
    except sql_exception.OperationalError:
        entry = blogDB.Post("General Error", "Whoops", "The server had a senior moment, or something like that.\
          Give it a minute and try again, and then contact the administrator", "")

    # if the entry doesn't exist, tell the user.
    if entry is None:
        flash("There are no posts with ID # " + request.args.get('entry') + " to be edited.")
        return redirect('/home')

    form = formread.BlogForm(request.form)

    # update the relevant parts of the post
    if request.method == 'POST':
        if form.delete.data is True:
            db.session.delete(entry)

        else:
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
                    entry.head_img = filename
                    flash("head image updated")

        # locate associated projects
        form_projects = form.projects.data
        entry.set_projects(form_projects)

        db.session.commit()
        return redirect('/home')

    else:
        # pre-populate the form:
        tags = ', '.join([tag.value for tag in entry.tags])

        form = formread.BlogForm(title=entry.title, textHTML=entry.content, tags=tags)

        projects = blogDB.Project.query.all()
        form.projects.choices = [(project.id, project.title) for project in projects]
        selected = [str(p.id) for p in entry.projects]
        form.projects.data = selected

    base = app.jinja_env.get_template('edit-post.html')
    return render_template(base, title="editing post", form=form, id=request.args.get('entry'))