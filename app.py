#!/usr/bin/python
from flask import Flask, render_template, url_for, redirect, flash, g
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

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# routes
@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # create a new user in the db
        User.create(
            username = form.username.data,
            email = form.email.data,
            password = md5(form.password.data).hexdigest()
        )

        flash('Thanks for registering')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            User.get(
                username = form.username.data,
                password = md5(form.password.data).hexdigest()
            )
        except User.DoesNotExist:
            flash('User doesnt exist')
        else:
            print 'logged in'
            flash('Logging in')

        return redirect(url_for('login'))

    return render_template('login.html', form=form)

# run app
if __name__ == '__main__':
    app.run(debug=True)
