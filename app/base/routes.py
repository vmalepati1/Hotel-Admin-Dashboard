# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import Users
import bcrypt
import uuid
import datetime

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form and login_form.validate():
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()
        
        # Check the password
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            user.last_login = datetime.datetime.utcnow()
            user.last_ip = request.environ['REMOTE_ADDR']
            db.session.commit()
            
            login_user(user, remember = ('remember_me' in request.form))
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'login/login.html', msg=_('Wrong user or password'), form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'login/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form and create_account_form.validate():
        username  = request.form['username']
        email     = request.form['email'   ]

        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template( 'login/register.html', msg=_('Username already registered'), form=create_account_form)

        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template( 'login/register.html', msg=_('Email already registered'), form=create_account_form)

        attrs = dict(request.form)
        attrs['salt'] = bcrypt.gensalt().decode() 
        attrs['is_admin'] = 0
        attrs['remember_token'] = str(uuid.uuid4())
        attrs['first_name'] = 'Lucky'
        attrs['last_name'] = 'Jesse'
        
        current_timestamp = datetime.datetime.utcnow()
        attrs['date_created'] = current_timestamp
        attrs['date_updated'] = current_timestamp
        
        # else we can create the user
        user = Users(**attrs)
        db.session.add(user)
        db.session.commit()

        return render_template( 'login/register.html', success=_('User created please <a href="/login">login</a>'), form=create_account_form)
    else:
        return render_template( 'login/register.html', form=create_account_form)

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    if not current_user.is_admin:
        abort(403)
        
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return _('Server shutting down...')

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
