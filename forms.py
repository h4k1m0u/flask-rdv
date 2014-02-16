#!/usr/bin/python
from wtforms import TextField, PasswordField, HiddenField, validators
from flask.ext.wtf import Form

class RegistrationForm(Form):
    username = TextField('Username', [validators.Required(), validators.length(min=3, max=25)])
    email = TextField('Email address', [validators.Required(), validators.Email()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password', [validators.Required()])
    form_name = HiddenField(default='register_form')

class LoginForm(Form):
    username = TextField('Username', [validators.Required(), validators.length(min=3, max=25)])
    password = PasswordField('Password', [validators.Required()])
    form_name = HiddenField(default='login_form')
