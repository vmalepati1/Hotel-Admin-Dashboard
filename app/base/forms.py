# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, Length
from flask_babel import lazy_gettext as _l

## login and registration

class LoginForm(FlaskForm):
    username = TextField    (_l('Username'),   id='username_login'   , validators=[DataRequired()])
    password = PasswordField(_l('Password'),   id='pwd_login'        , validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'), id='remember_me_login')

class CreateAccountForm(FlaskForm):
    username = TextField(_l('Username')     , id='username_create' , validators=[DataRequired(), Length(max=45)])
    email    = TextField(_l('Email')        , id='email_create'    , validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField(_l('Password') , id='pwd_create'      , validators=[DataRequired(), Length(max=255)])
