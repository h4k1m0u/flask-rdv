#register!/usr/bin/python
from flask import Flask, render_template, url_for, redirect, flash, g, session, request, jsonify
from functools import wraps
from forms import RegistrationForm, LoginForm
from models import database, User, Rdv
from hashlib import md5
import os
from datetime import datetime

# config 
CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

# create app 
app = Flask(__name__)
app.config.from_object(__name__)

# connection to db
@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# session-based authentication
def authenticate(user):
    session['is_logged_in'] = True
    session['username'] = user.username

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('is_logged_in'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return inner

# routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # login & register forms
    login_form = LoginForm(prefix='login') 
    register_form  = RegistrationForm(prefix='register') 
    is_logged_in = session.get('is_logged_in')
    username = session.get('username')

    # on login form submission
    if login_form.form_name.data == 'login_form' and login_form.validate_on_submit():
        # check if user exists in db
        try:
            user = User.get(
                username = login_form.username.data,
                password = md5(login_form.password.data).hexdigest()
            )
        except User.DoesNotExist:
            flash('User doesnt exist')
        else:
            # authenticate user
            authenticate(user)

            flash('Logging in')
            return redirect(url_for('rdv'))

    # on register form submission
    if register_form.form_name.data == 'register_form' and register_form.validate_on_submit():
        # create a new user in the db
        User.create(
            username = register_form.username.data,
            email = register_form.email.data,
            password = md5(register_form.password.data).hexdigest()
        )

        flash('Thanks for registering')
        return redirect(url_for('rdv'))

    return render_template('register.html', **{
        'login_form':       login_form,
        'register_form':    register_form,
        'is_logged_in':     is_logged_in,
        'username':         username,
        'getmtime':         os.path.getmtime
    })

@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    flash('You were logged out')

    return redirect(url_for('index'))

@app.route('/rdv')
@login_required
def rdv():
    return render_template('rdv.html', **{
        'is_logged_in': session.get('is_logged_in'),
        'username':     session.get('username'),
        'getmtime':     os.path.getmtime
    })

@app.route('/save_rdv')
@login_required
def save_rdv():
    title = request.args.get('title', None, type=str)
    start = datetime.strptime(request.args.get('start', None, type=str), "%a, %d %b %Y %H:%M:%S %Z")
    end = datetime.strptime(request.args.get('end', None, type=str), "%a, %d %b %Y %H:%M:%S %Z")

    # save rdv (event) to the db
    Rdv.create(
        title = title,
        start = start,
        end =   end
    )

    return jsonify(flash="Rdv '%s' added between %s and %s" % (title, start, end))

# run app
if __name__ == '__main__':
    app.run(debug=True)
