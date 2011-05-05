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
  lastSignUp = db.DateTimeProperty()

  #end of User properties
