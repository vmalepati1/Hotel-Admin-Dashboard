# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app import db
from app.home import blueprint
from app.home.forms import EditProfileForm, EditHotelForm
from app.home.models import Hotel
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import requests
import json

@blueprint.route('/index')
@login_required
def index():
    return redirect(url_for('home_blueprint.edit_profile'))

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_form = EditProfileForm(request.form)
    
    if 'save' in request.form:
        if edit_form.validate():
            current_user.username = request.form['username']
            current_user.email = request.form['email']
            current_user.first_name = request.form['first_name']
            current_user.last_name = request.form['last_name']

            db.session.commit()
        
            return render_template('profile.html', success='Changes successfully saved!', form=edit_form)
        else:
            return render_template('profile.html', msg='Failed to save changes! Please check below.', form=edit_form)
    else:
        return render_template('profile.html', form=edit_form)

@blueprint.route('/hotels_select',  methods=['GET', 'POST'])
@login_required
def select_hotel():
    if request.method == "POST":
        if 'delete' in request.form:
            hotel_to_delete = Hotel.query.filter_by(seq_id=request.form['delete']).first()

            db.session.delete(hotel_to_delete)
            db.session.commit()

    if current_user.is_admin:
        hotels = Hotel.query.all()
    else:
        hotels = Hotel.query.filter_by(author=current_user.id).all()
        
    num_hotels = len(hotels)
    
    return render_template('hotels_select.html', hotels=hotels, num_hotels=num_hotels)

@blueprint.route('/edit_hotel/<int:hotel_id>', methods=['GET', 'POST'])
@login_required
def edit_hotel(hotel_id):
    edit_form = EditHotelForm(request.form)

    hotel = Hotel.query.filter_by(seq_id=hotel_id).first()

    if 'save' in request.form:
        if edit_form.validate_on_submit():
            return render_template('edit_hotel.html', success='Changes successfully saved!', hotel=hotel, form=edit_form)
        else:
            return render_template('edit_hotel.html', msg='Failed to save changes! Please check below.', hotel=hotel, form=edit_form)
    
    return render_template('edit_hotel.html', hotel=hotel, form=edit_form)
    
@blueprint.route('/<template>')
def route_template(template):

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    try:

        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('error-404.html'), 404
    
    except:
        return render_template('error-500.html'), 500
