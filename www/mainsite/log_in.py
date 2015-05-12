__author__ = 'BroZapp'

def verify_log_in(app):
        # make sure user is logged in
    if 'user' not in app.session:
        flash('please log in to post')
        return redirect('/log-in')
