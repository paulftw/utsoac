from google.appengine.ext import db

class Activity(db.Model):
    title = db.StringProperty(required = True)
    description = db.TextProperty()
    when = db.DateTimeProperty(auto_now_add = True)
    owner = db.StringProperty(required = True)
    participants = db.IntegerProperty(required = True)