from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class EditProfileForm(FlaskForm):

    username = TextField    ('Username', [Length(max=45)])
    email = TextField       ('Email address', [Email(), Length(max=255)])
    first_name = TextField  ('First name', [Length(max=150)])
    last_name = TextField   ('Last name', [Length(max=150)])

class EditHotelForm(FlaskForm):

    id = TextField                          ('Booking code ID', [Length(max=20)])
    order_id = IntegerField                 ('Order ID')
    name = TextField                        ('Accommodation name', [Length(max=100)])
    rating = TextField                      ('Structure rating', [Length(max=20)])
    address = TextField                     ('Address (including city)', [Length(max=100)])
    zip = TextField                         ('CAP or ZIP code', [Length(max=10)])
    town = TextField                        ('Town', [Length(max=50)])
    sidecode = TextField                    ('Geolocal Portal Code', [Length(max=11)])
    country = TextField                     ('Country', [Length(max=50)])
    hotel_smalldesc = TextField             ('Hotel short description', [Length(max=255)])
    arrival = TextField                     ('Arrival times', [Length(max=50)])
    departure = TextField                   ('Departure times', [Length(max=50)])
    location = TextField                    ('Location', [Length(max=50)])
    website = TextField                     ('Website', [Length(max=500)])
    phone = TextField                       ('Phone', [Length(max=100)])
    numero_stelle = SelectField             ('Number of stars', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    tipologia_struttura = SelectField       ('Type of structure', choices=[('Hotel room', 'Hotel room'), ('Villa', 'Villa')])
