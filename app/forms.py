from wtforms import StringField, PasswordField, validators, SubmitField
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