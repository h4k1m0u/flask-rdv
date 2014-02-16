#register!/usr/bin/python
from flask import Flask, render_template, url_for, redirect, flash, g, session, request
from forms import RegistrationForm, LoginForm
from models import database, User
from hashlib import md5
import os

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

# routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # login & register forms
    login_form = LoginForm(prefix='login') 
    register_form  = RegistrationForm(prefix='register') 
    is_logged_in = session.get('is_logged_in')

    # on login form submission
    if login_form.validate_on_submit():
        # check if user exist in db
        try:
            user = User.get(
                username = login_form.username.data,
                password = md5(login_form.password.data).hexdigest()
            )
        except User.DoesNotExist:
            flash('User doesnt exist')
        else:
            print 'logged in'
            flash('Logging in')
            authenticate(user)

    # on register form submission
    if register_form.validate_on_submit():
        print 'register form validation', register_form.form_name.data
        # create a new user in the db
        User.create(
            username = register_form.username.data,
            email = register_form.email.data,
            password = md5(register_form.password.data).hexdigest()
        )

        flash('Thanks for registering')

    return render_template('register.html', **{
        'login_form': login_form,
        'is_login_form': login_form.form_name.data == 'login_form',
        'register_form': register_form,
        'is_register_form': register_form.form_name.data == 'register_form',
        'is_logged_in': is_logged_in
    })

# run app
if __name__ == '__main__':
    app.run(debug=True)
