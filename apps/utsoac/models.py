from google.appengine.ext import db

from tipfy.ext.auth.model import User as TipfyUser

class Activity(db.Model):
  title = db.StringProperty(required = True)
  description = db.TextProperty()
  date = db.DateProperty(auto_now_add = True)
  owner = db.StringProperty(required = True)
  participants = db.IntegerProperty(required = True)

class Join(db.Model):
  weight = db.IntegerProperty(required = True)

class User(TipfyUser):
  firstName = db.StringProperty()
  lastName = db.StringProperty()
  dob = db.DateProperty()
  health = db.StringProperty()
  lastSignUp = db.DateTimeProperty()

class Address(db.Model):
  streetAddr = db.StringProperty(required = True)
  suburb = db.StringProperty(required = True)
  zipcode = db.StringProperty(required = True)
  state = db.StringProperty(required = True)
  country = db.StringProperty(required = True)
