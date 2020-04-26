from wtforms import StringField, PasswordField, validators, SubmitField,DateField,IntegerField,SelectField,BooleanField,RadioField

# from wtforms.widgets import HiddenInput
from wtforms.widgets.html5 import NumberInput

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from flask_wtf import FlaskForm
from app.database.models import User

class RegistrationForm(FlaskForm):

  def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user is not None:
          raise ValidationError('The username already exists.')

  def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is not None:
          raise ValidationError('The email already exists.')

  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email(message=('Please enter a valid email address.'))])
  password = PasswordField('Password', validators=[DataRequired(),
                            Length(min=6, message=('Password must be greater than 6 characters.')),
                            EqualTo('password2', message='Passwords must match')])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired()])
  submit = SubmitField('Register')


class LoginForm(FlaskForm):
  def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is None:
          raise ValidationError('The email doesnot exists.')

  email = StringField('Email', validators=[DataRequired(), Email(message=('Please enter a valid email address.'))])
  password = PasswordField('Password', validators=[DataRequired(),
                            Length(min=6, message=('Invalid credentials.'))
                            ])
  submit = SubmitField('Login')





class EditProfileForm(FlaskForm):
  name = StringField('name')
  # dob= DateField('DOB',format='%Y-%m-%d')
  age=IntegerField(widget=NumberInput())
  contact_email1 = StringField('contactemail1', validators=[Email(message=('Please enter a valid email address.'))])
  contact_phone1 = StringField('contactphone1',validators=[Length(max=17, message=('Phone number too long')) ])
 
  link_instagram = StringField('linkinstagram',validators=[Length(max=500, message=('Link too long')) ])
  link_tiktok = StringField('linktiktok',validators=[Length(max=500, message=('Link too long')) ])
 
  ideal_advertisers = StringField('idealadvertisers',validators=[Length(max=2000, message=('Too many advertisers')) ])
  number_of_followers_instagram= IntegerField(widget=NumberInput(),validators=[Optional()])
  number_of_followers_tiktok= IntegerField(widget=NumberInput(),validators=[Optional()])
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


FAMILARITY_OPTIONS = [
# (-1, 'Choose...'),
("", 'Choose'),
("Extremely Familiar", 'Extremely Familiar'),
("Very Familiar", 'Very Familiar'),
("Somewhat Familiar", 'Somewhat Familiar'),
("Not So Familiar", 'Not So Familiar'),
("Not at all Familiar", 'Not at all Familiar')]
# dd_car_makes = SelectField('dd_car_makes', choices=FAMILARITY_OPTIONS,
# validators=[DataRequired()])


class EditNewProfileForm(FlaskForm):
  class Meta:
      all_fields_optional = True
  # def dropdown_required(form, field):
  # def dropdown_required(self, field):
  #   print("validating and the option is ")
  #   print(field.data)
  #   if field.data == -1:
  #     raise ValidationError('Please choose an option')

  name = StringField('name')
  age=IntegerField(widget=NumberInput())

  # gender =StringField('gender',validators=[Length(max=1, message=('Too long gender')) ])
  gender =RadioField('gender', choices=[('0','Male'), ('1','Female'), ('2','Other')],validators=[Optional()])

  # dob= DateField('DOB',format='%Y-%m-%d')
  contact_email1 = StringField('contactemail1', validators=[Optional(),Email(message=('Please enter a valid email address.'))],default=None)
  contact_phone1 = StringField('contactphone1',validators=[Optional(),Length(max=17, message=('Phone number too long')) ])
 
  link_instagram = StringField('linkinstagram',validators=[Length(max=500, message=('Link too long')) ])
  link_tiktok = StringField('linktiktok',validators=[Length(max=500, message=('Link too long')) ])
  link_firework = StringField('linkfirework',validators=[Length(max=500, message=('Link too long')) ])
  link_kwai = StringField('linkkwai',validators=[Length(max=500, message=('Link too long')) ])

  # familarity_with_instagram = SelectField('familarityinstagram', choices=FAMILARITY_OPTIONS, validators=[DataRequired(),dropdown_required]) 
  familarity_with_instagram = SelectField('familarityinstagram', choices=FAMILARITY_OPTIONS, validators=[Optional()]) 
  familarity_with_tiktok = SelectField('familaritytiktok', choices=FAMILARITY_OPTIONS, validators=[Optional()]) 
  familarity_with_kwai = SelectField('familaritykwai', choices=FAMILARITY_OPTIONS, validators=[Optional()]) 
  familarity_with_triller = SelectField('familaritytriller', choices=FAMILARITY_OPTIONS, validators=[Optional()]) 

  ideal_advertisers = StringField('idealadvertisers',validators=[Length(max=2000, message=('Too many advertisers')) ])
  
  number_of_followers_instagram= IntegerField(widget=NumberInput(),validators=[Optional()])
  number_of_followers_tiktok= IntegerField(widget=NumberInput(),validators=[Optional()])
  number_of_followers_triller= IntegerField(widget=NumberInput(),validators=[Optional()])
  number_of_followers_kwai= IntegerField(widget=NumberInput(),validators=[Optional()])

  submit = SubmitField('Submit')



  is_user_content_creator = BooleanField('Content Creator?',default=False,
                      false_values=('False', 'false', ''))
  # is_user_content_creator = BooleanField('', widget=HiddenInput(), default=False,false_values=('False', 'false', ''))

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
