from google.appengine.ext import db

class Activity(db.Model):
  title = db.StringProperty(required = True)
  description = db.TextProperty()
  date = db.DateProperty(auto_now_add = True)
  owner = db.StringProperty(required = True)
  participants = db.IntegerProperty(required = True)
