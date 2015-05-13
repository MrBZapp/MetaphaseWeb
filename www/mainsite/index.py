from flask import Flask, \
    jsonify, \
    render_template, \
    redirect, \
    request, \
    flash, \
    session,\
    Markup

from blogread import db as db
from sqlalchemy import exc as sql_exception
import blogread
import formread
import hashlib
import os
import werkzeug

# Global definitions
GLOBAL_ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Static Subfolder names
POST_IMG_FOLDER = 'static/posts/img/'
POST_TMP_FOLDER = '/static/posts/tmp'

# Config dependent paths
#DATABASE_URI = 'mysql+pymysql://root:m3tadmin@localhost/blogdata' #Production
DATABASE_URI = 'mysql+pymysql://admin:admin@192.168.1.126/blogdata' #Dev

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in GLOBAL_ALLOWED_EXTENSIONS
# Define the app so we can assign some variables
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['POST_IMG_FOLDER'] = POST_IMG_FOLDER
app.config['POST_TMP_FOLDER'] = POST_TMP_FOLDER
db.init_app(app)

# set the secret key.  keep this really secret:
app.secret_key = '512cgv&P<T$$(){KMhb637rf6tn{_ube532v55@15-sdfgnhyr76'

@app.route('/')
def index():
    entries = [blogread.entry("General Error", "Whoops", "If you're seeing this, it's bad.  Write to this guy, he'll figure it out: sysadmin@metaphase.com", "")]
    try:
        entries = blogread.entry.query.all()
    except sql_exception.OperationalError:
        entries = [blogread.entry("Server", "Whoops", "The server forgot to provide any data or something,\
            we're not positive yet. <br> Give it a shot again but please cool it contact the system administrator if the problem persists.", "")]
        pass
        
    if entries is not None:
        for entry in entries:
            entry.content = Markup(entry.content)
        # may those that are last, be first.
        entries.reverse()
    return render_template('base.html', title="home", posts=entries, bootstrap=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = formread.RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = blogread.User(form.username.data, form.realname.data, form.email.data, form.password.data)
        session['user'] = user.username
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect('/')
    return render_template('register.html', form=form, bootstrap=True)


@app.route('/log-in', methods=['GET', 'POST'])
def log_in():
    form = formread.LogInForm(request.form)
    if request.method == 'POST':
        new_user = blogread.User.query.filter_by(username=str(form.username.data)).first()

        if new_user is None:
            flash("no user by that name")
            return redirect('/log-in')

        test_hash = hashlib.sha224(form.username.data + form.password.data).hexdigest()

        if new_user._hash == test_hash:
            user = {'uname': new_user.username,
                    'rname': new_user.realname,
                    'e-mail': new_user.email,
                    'admin': new_user._admin}

            session['user'] = user
            flash("Logged in")
            return redirect('/')
        else:
            flash("username or password is incorrect")

    return render_template('log-in.html', form=form, bootstrap=True)

@app.route('/log-out')
def log_out():
    session.pop('user')
    flash('logged out!')
    return redirect('/')


@app.route('/post', methods=['GET', 'POST'])
def post():
    # make sure user is logged in
    if 'user' not in session:
        flash('please log in to post')
        return redirect('/log-in')

    user = session['user']

    # if the user is trying to post, make sure they have the credentials.
    if user['admin'] == 1:
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
                    headIMG.save(os.path.join(app.config['POST_IMG_FOLDER'], filename))
                    flash('file submitted')
                else:
                    flash('If a file was submitted it was of a non-allowed format.')

            # add the entry to the database
            entry = blogread.entry(author=session['user']['rname'], title=form.title.data, content=content, imgpath=filename)
            try:
                db.session.add(entry)
                db.session.commit()
                return redirect('/')
            except sql_exception.OperationalError:
                flash('Post was not able to be submitted due to a server error.  Maybe try again?')

        base = app.jinja_env.get_template('makepost.html')
        return render_template(base, title="entering post", form=form, bootstrap=True)
    else:
        flash('You must have administrative rights to do that.')
        return redirect('log-in')


@app.route('/edit-post', methods=['GET', 'POST'])
def edit_post():
    # make sure user is logged in
    if 'user' not in session:
        flash('please log in to post')
        return redirect('/log-in')

    user = session['user']

    if user['admin'] == 1:
        # pull the entry from the database
        try:
            entry = blogread.entry.query.filter_by(id=request.args.get('entry')).first()
        except sql_exception.OperationalError:
            entry = blogread.entry("General Error", "Whoops", "The server had a senior moment, or something like that.\
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

                # if a file is provided and it's legit, replace it
                if headIMG != "" and allowed_file(headIMG.filename):
                    # write the new file
                    filename = werkzeug.secure_filename(headIMG.filename)
                    headIMG.save(os.path.join(app.config['POST_IMG_FOLDER'], filename))

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
        flash('You must be logged-in as an administrator to do that.')
        return redirect('log_in')


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    return request.args.get('comments')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




# @app.route('/mastering')
# def master():
#     base = app.jinja_env.get_template('mastering/master.html')
#     return render_template(base, title="Very Good Mastering", bootstrap=True)
