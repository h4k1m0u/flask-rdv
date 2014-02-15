#!/usr/bin/python
from wtforms import BooleanField, TextField, PasswordField, validators
from flask.ext.wtf import Form

class RegistrationForm(Form):
    username = TextField('Username', [validators.length(min=4, max=25)])
    email = TextField('Email address', [validators.length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
