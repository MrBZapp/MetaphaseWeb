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



POST_IMG_FOLDER = 'C:\Users\BroZapp\mainsite\git\www\mainsite\posts\img'
POST_TMP_FOLDER = 'C:\Users\BroZapp\mainsite\git\www\mainsite\posts\tmp'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['POST_IMG_FOLDER'] = POST_IMG_FOLDER
app.config['POST_TMP_FOLDER'] = POST_TMP_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:m3tadmin@localhost/blogdata'
db.init_app(app)

# set the secret key.  keep this really secret:
app.secret_key = '512cgv&P<T$$(){KMhb637rf6tn{_ube532v55@15-sdfgnhyr76'

@app.route('/')
def index():
    entries = [blogread.entry("Server", "Error", "There was an error fetching data from the server,\
            we apologize for the inconvenience. <br> Please contact the system administrator if the problem persists.", "")]
    try:
        entries = blogread.entry.query.all()
    except sql_exception.OperationalError:
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
        if request.method == 'POST':
            # import the html text
            if 'bodyHTML'not in request.files or form.textHTML.data == "":
                content = form.textHTML.data
            else:
                bodyHTML = request.files['bodyHTML']
                content = bodyHTML.read()
            
            # get header image
            if 'headIMG' in request.files:
                headIMG = request.files['headIMG']
                if headIMG and allowed_file(headIMG.filename):
                    filename = werkzeug.secure_filename(headIMG.filename)
                    headIMG.save(os.path.join(POST_IMG_FOLDER, filename))
                    flash('file submitted')
            else:
                filename = ""           
            # add the entry to the database
            entry = blogread.entry(author=session['user']['rname'], title=form.title.data, content=content, imgpath=filename)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

        base = app.jinja_env.get_template('makepost.html')
        return render_template(base, title="entering post", form=form, bootstrap=True)
    else:
        flash('You must have administrative rights to do that.')
        return redirect('log-in')


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    return request.args.get('comments')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




# @app.route('/mastering')
# def master():
#     base = app.jinja_env.get_template('mastering/master.html')
#     return render_template(base, title="Very Good Mastering", bootstrap=True)
