from tipfy.ext.wtforms import Form, validators
from tipfy.ext.wtforms.fields import TextField, PasswordField, BooleanField, IntegerField, DateField

REQUIRED = validators.Required()
AUPHONE = validators.Regexp('(\d\s*){10}')


class LoginForm(Form):
  loginid = TextField('E-mail', validators=[REQUIRED, validators.Email()])
  password = PasswordField('Password', validators=[REQUIRED])
  remember = BooleanField('Keep me signed in')


# SignupForm - sign in for users logged in via OpenID
class SignupForm(Form):
  pass


class RegistrationForm(Form):
  loginid = TextField('E-mail', validators=[REQUIRED, validators.Email()])
  password = PasswordField('Password', validators=[REQUIRED])
  password_confirm = PasswordField('Confirm the password', validators=[REQUIRED])

  firstName = TextField('First Name', validators=[REQUIRED])
  lastName = TextField('Last Name', validators=[REQUIRED])
  dob = DatetField('Date of birth', display_format='%d-%M-%Y', validators=[REQUIRED])
  contactPhone = TextField('Mobile Phone', validators=[REQUIRED, AUPHONE])
  health = TextAreaField('Health/Special needs (visible to trip leaders)')
  outdoorExperience = TextAreaField('Experience in Climbing/Canyoning/Hiking')


class NewActivityForm(Form):
  title = TextField('Short description', validators=[REQUIRED])
  date = DateField('Start date', format='%d/%m/%Y', validators=[REQUIRED])
  description = TextAreaField('Full activity details')
  participants = IntegerField('Participants (including you)', validators=[REQUIRED])
  contactPhone = TextField(required = True, validators=[REQUIRED, AUPHONE])
  instructions_for_joined = TextAreaField('Welcome text (meeting location, payment details, requests for additional info)')
