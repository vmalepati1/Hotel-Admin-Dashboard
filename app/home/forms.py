from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_babel import lazy_gettext as _l

class EditProfileForm(FlaskForm):

    username = TextField    (_l('Username'), [Length(max=45)])
    email = TextField       (_l('Email address'), [Email(), Length(max=255)])
    first_name = TextField  (_l('First name'), [Length(max=150)])
    last_name = TextField   (_l('Last name'), [Length(max=150)])

class EditHotelForm(FlaskForm):

    id = TextField                          (_l('Booking code ID'), [Length(max=20)])
    order_id = IntegerField                 (_l('Order ID'))
    name = TextField                        (_l('Accommodation name'), [Length(max=100)])
    rating = TextField                      (_l('Structure rating'), [Length(max=20)])
    address = TextField                     (_l('Address (including city)'), [Length(max=100)])
    zip = TextField                         (_l('CAP or ZIP code'), [Length(max=10)])
    town = TextField                        (_l('Town'), [Length(max=50)])
    sidecode = TextField                    (_l('Geolocal Portal Code'), [Length(max=11)])
    country = TextField                     (_l('Country'), [Length(max=50)])
    hotel_smalldesc = TextField             (_l('Hotel short description'), [Length(max=255)])
    arrival = TextField                     (_l('Arrival times'), [Length(max=50)])
    departure = TextField                   (_l('Departure times'), [Length(max=50)])
    location = TextField                    (_l('Location'), [Length(max=50)])
    website = TextField                     (_l('Website'), [Length(max=500)])
    phone = TextField                       (_l('Phone'), [Length(max=100)])
    numero_stelle = SelectField             (_l('Number of stars'), choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    tipologia_struttura = SelectField       (_l('Type of structure'), choices=[('Hotel room', 'Hotel room'), ('Villa', 'Villa')])
