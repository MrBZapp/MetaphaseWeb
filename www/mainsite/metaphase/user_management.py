__author__ = 'BroZapp'
import hashlib
from flask import flash, redirect, render_template, request, session
from metaphase import app, db, formread, blogread


def verify_user_log_in():
    # make sure user is logged in
    if 'user' not in session:
        flash('please log in to post')
        return redirect('/log-in')


def verify_user_admin():
    if session['user']['admin'] != 1:
        flash('You require administrative rights to do that.')
        return False
    return True

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
            user = {'username': new_user.username,
                    'realname': new_user.realname,
                    'email': new_user.email,
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