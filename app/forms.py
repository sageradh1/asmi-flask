from wtforms import StringField, PasswordField, validators, SubmitField,DateField,IntegerField

from wtforms.widgets.html5 import NumberInput

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from flask_wtf import FlaskForm
from app.database.models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email(message=('Please enter a valid email address.'))])
  password = PasswordField('Password', validators=[DataRequired(),
                            Length(min=6, message=('Password must be greater than 6 characters.')),
                            EqualTo('password2', message='Passwords must match')])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired()])
  submit = SubmitField('Register')

  def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user is not None:
          raise ValidationError('The username already exists.')

  def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is not None:
          raise ValidationError('The email already exists.')



class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email(message=('Please enter a valid email address.'))])
  password = PasswordField('Password', validators=[DataRequired(),
                            Length(min=6, message=('Invalid credentials.'))
                            ])
  submit = SubmitField('Login')

  def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is None:
          raise ValidationError('The email doesnot exists.')




class EditProfileForm(FlaskForm):
  name = StringField('name')
  dob= DateField('DOB',format='%Y-%m-%d')
  contact_email1 = StringField('contactemail1', validators=[Email(message=('Please enter a valid email address.'))])
  contact_phone1 = StringField('contactphone1',validators=[Length(max=17, message=('Phone number too long')) ])
  link_instagram = StringField('linkinstagram',validators=[Length(max=500, message=('Link too long')) ])
  link_tiktok = StringField('linktiktok',validators=[Length(max=500, message=('Link too long')) ])
  ideal_advertisers = StringField('idealadvertisers',validators=[Length(max=2000, message=('Too many advertisers')) ])
  reach= IntegerField(widget=NumberInput())
  submit = SubmitField('Save Changes')


  def is_valid_phone(self, contactphone1):
      try:
          p = phonenumbers.parse(contactphone1.data)
          if not phonenumbers.is_valid_number(p):
              return False
          return True
      except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
          raise False

  def validate_phone(self, contactphone1):
      try:
          p = phonenumbers.parse(contactphone1.data)
          if not phonenumbers.is_valid_number(p):
              raise ValueError()
      except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
          raise ValidationError('Invalid phone number')
