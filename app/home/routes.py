# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from config import Config
from app import db
from app.home import blueprint
from app.home.forms import EditProfileForm, EditHotelForm
from app.home.models import Hotel, Images
from app.home.utils import validate_image
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import requests
import json
from werkzeug.utils import secure_filename
import uuid
import os
from urllib.parse import urljoin

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
        
            return render_template('profile.html', success=_('Changes successfully saved!'), form=edit_form)
        else:
            return render_template('profile.html', msg=_('Failed to save changes! Please check below.'), form=edit_form)
    else:
        return render_template('profile.html', form=edit_form)

@blueprint.route('/hotels_select',  methods=['GET', 'POST'])
@login_required
def select_hotel():
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
    images = Images.query.filter_by(hotel_id=hotel_id).all()

    if 'save' in request.form:
        if edit_form.validate_on_submit():
            ignore_fields = ['seq_id', 'author', 'cover_image']
            
            for name in hotel.__dict__.keys():
                if name.startswith('_') or name in ignore_fields:
                    continue

                if name in edit_form.__dict__.keys():
                    setattr(hotel, name, getattr(edit_form, name).data)
                else:
                    setattr(hotel, name, request.form[name])

            uploaded_file = request.files['cover_image_file']
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                
                if file_ext.upper() not in (ext.upper() for ext in Config.UPLOAD_EXTENSIONS) or \
                        file_ext.upper() != validate_image(uploaded_file.stream).upper():
                    return render_template('edit_hotel.html', msg=_('Failed to upload cover image!'), hotel=hotel, form=edit_form)

                filename = str(uuid.uuid4()) + file_ext

                relative_path = url_for('static', filename=Config.UPLOAD_STATIC_FOLDER_PATH + '/' + filename)
                absolute_path = os.path.join(Config.UPLOAD_FILE_PATH, filename)
                
                uploaded_file.save(absolute_path)

                image_url = urljoin(request.url_root, relative_path)
                
                hotel.cover_image = image_url

            db.session.commit()

            return render_template('edit_hotel.html', success=_('Changes successfully saved!'), hotel=hotel, images=images, form=edit_form)
        else:
            return render_template('edit_hotel.html', msg=_('Failed to save changes! Please check below.'), hotel=hotel, images=images, form=edit_form)

    elif 'delete_image' in request.form:
        image_to_delete = Images.query.filter_by(id=request.form['delete_image']).first()

        db.session.delete(image_to_delete)
        db.session.commit()

    elif 'add_image' in request.form:
        uploaded_file = request.files['gallery_image_file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            
            if file_ext.upper() not in (ext.upper() for ext in Config.UPLOAD_EXTENSIONS) or \
                    file_ext.upper() != validate_image(uploaded_file.stream).upper():
                return render_template('edit_hotel.html', msg=_('Failed to upload gallery image!'), hotel=hotel, images=images, form=edit_form)

            filename = str(uuid.uuid4()) + file_ext

            relative_path = url_for('static', filename=Config.UPLOAD_STATIC_FOLDER_PATH + '/' + filename)
            absolute_path = os.path.join(Config.UPLOAD_FILE_PATH, filename)
            
            uploaded_file.save(absolute_path)

            image_url = urljoin(request.url_root, relative_path)
            
            new_image = Images()
            new_image.filepath = image_url
            new_image.hotel_id = hotel_id

            db.session.add(new_image)
            db.session.commit()

    images = Images.query.filter_by(hotel_id=hotel_id).all()
    return render_template('edit_hotel.html', hotel=hotel, images=images, form=edit_form)

@blueprint.route('/create_hotel')
@login_required
def create_hotel():
    new_hotel = Hotel()
    new_hotel.author = current_user.id

    db.session.add(new_hotel)
    db.session.commit()

    return redirect(url_for('home_blueprint.edit_hotel', hotel_id=new_hotel.seq_id))
    
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
