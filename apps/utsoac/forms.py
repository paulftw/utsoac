from tipfy.ext.wtforms import Form, validators
from tipfy.ext.wtforms.fields import TextField, PasswordField, BooleanField, IntegerField, \
    DateField, TextAreaField, HiddenField

REQUIRED = validators.Required()
AUPHONE = validators.Regexp('(\d\s*){10}')


class LoginForm(Form):
  loginid = TextField('E-mail', validators=[REQUIRED, validators.Email()])
  password = PasswordField('Password', validators=[REQUIRED])
  remember = BooleanField('Keep me signed in')


# SignupForm - sign in for users logged in via OpenID
class SignupForm(Form): pass

class RegistrationForm(Form):
  loginid = TextField('E-mail', validators=[REQUIRED, validators.Email()])
  password = PasswordField('Password', validators=[REQUIRED])
  password_confirm = PasswordField('Confirm the password', validators=[REQUIRED])

  first_name = TextField('First Name', validators=[REQUIRED])
  last_name = TextField('Last Name', validators=[REQUIRED])
  dob = DateField('Date of birth', format='%d/%m/%Y', validators=[REQUIRED])
  contact_phone = TextField('Mobile Phone', validators=[REQUIRED, AUPHONE])
  health = TextAreaField('Health/Special needs (visible to trip leaders)')
  experience = TextAreaField('Experience in Climbing/Canyoning/Hiking')


class NewActivityForm(Form):
  activity_id = HiddenField()
  title = TextField('Short description', validators=[REQUIRED])
  date = DateField('Start date', format='%d/%m/%Y', validators=[REQUIRED])
  description = TextAreaField('Full activity details')
  participants = IntegerField('Participants (including you)', validators=[REQUIRED])
  contact_phone = TextField('Contact Phone', validators=[REQUIRED, AUPHONE])
  instructions = TextAreaField('Welcome text'
      ' (meeting location, payment details, requests for additional info)')


class JoinActivityForm(Form):
  activity = HiddenField()
  phone = TextField('Contact Phone', validators=[REQUIRED, AUPHONE])
  car = BooleanField('I can bring my own car')
  gear = TextAreaField('Gear you need')
  comments = TextAreaField('Any comments')
  weaver = BooleanField('I agree to the following disclaimer')