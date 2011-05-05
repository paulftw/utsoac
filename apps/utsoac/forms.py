from tipfy.ext.wtforms import Form, fields, validators

REQUIRED = validators.Required()

class LoginForm(Form):
  loginid = fields.TextField('Login or e-mail', validators=[REQUIRED, validators.Email()])
  password = fields.PasswordField('Password', validators=[REQUIRED])
  remember = fields.BooleanField('Keep me signed in')

class SignupForm(Form):
  nickname = fields.TextField('Nickname', validators=[REQUIRED])
  dob = fields.TextField('Date of birth', display_format='%d-%M-%Y')

class RegistrationForm(Form):
  loginid = fields.TextField('e-mail', validators=[REQUIRED])
  password = fields.PasswordField('Password', validators=[REQUIRED])
  password_confirm = fields.PasswordField('Confirm the password', validators=[REQUIRED])


class NewActivityForm(Form):
  title = fields.TextField('Short description', validators=[REQUIRED])
  date = fields.DateField('Start date', format='%d/%m/%Y', validators=[REQUIRED])
  description = fields.TextAreaField('Full activity details')
  participants = fields.IntegerField('Participants (including you)', validators=[REQUIRED])
  instructions_for_joined = fields.TextAreaField('Welcome text (meeting location, payment details, requests for additional info)')
