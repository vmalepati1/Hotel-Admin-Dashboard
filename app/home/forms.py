from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, Length

class EditProfileForm(FlaskForm):

    username = TextField    ('Username', [Length(max=45)])
    email = TextField       ('Email address', [Email(), Length(max=255)])
    first_name = TextField  ('First name', )
