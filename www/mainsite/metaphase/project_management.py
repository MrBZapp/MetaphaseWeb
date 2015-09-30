__author__ = 'BroZapp'

from flask import flash, redirect, render_template, request
from metaphase import app, db, formread, blogDB, user_management as UM
from _file_helpers import allowed_file
from sqlalchemy import exc as sql_exception
import werkzeug
import os

@app.route('/projects')
def projects():
    project_id = request.args.get('post_id')
    base = app.jinja_env.get_template('projects.html')

    if project_id is not None:
        pass
    else:
        project_list = blogDB.Project.query.all()

    if project_list is not None:
        project_list.reverse()
    return render_template(base, title="projects", projects=project_list, bootstrap=True)

@app.route('/create-project', methods=['GET', 'POST'])
def create_project():
    # make sure user is logged in
    UM.verify_user_log_in()

    # if the user is trying to post, make sure they have the credentials.
    UM.verify_user_admin()

    # set up the page properly
    form = formread.ProjectForm(request.form)
    base = app.jinja_env.get_template('makeproject.html')

    # if we're submitting the form as opposed to requesting it do these things.
    if request.method == 'POST':
        # get header image
        if 'headIMG' in request.files:
            headIMG = request.files['headIMG']

            # if the file is legit replace the filename with it
            if headIMG and allowed_file(headIMG.filename):
                file_name = werkzeug.secure_filename(headIMG.filename)
                headIMG.save(os.path.join(app.root_path, app.config['PROJECT_IMG_FOLDER'], file_name))
                flash('file submitted. ')
            else:
                flash('If a file was submitted, it was of a non-allowed format.')
                return render_template(base, title="creating project", form=form, bootstrap=True)


        # add the entry to the database
        entry = blogDB.Project(title=form.title.data, pict=file_name, abstract=form.abstract.data)
        try:
            db.session.add(entry)
            db.session.commit()
            return redirect('/')
        except sql_exception.OperationalError:
            flash('Post was not able to be submitted due to a server error.  Maybe try again?')


    return render_template(base, title="creating project", form=form, bootstrap=True)