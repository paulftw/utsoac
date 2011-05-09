from google.appengine.ext import db

from datetime import datetime

from tipfy.ext.auth.model import User as TipfyUser

class Activity(db.Model):
  title = db.StringProperty(required = True)
  description = db.TextProperty()
  date = db.DateProperty(auto_now_add = True)
  created = db.DateTimeProperty(auto_now_add = True)
  owner = db.StringProperty(required = True)
  participants = db.IntegerProperty(required = True)
  
  @classmethod
  def create(cls, author, **args):
    now = datetime.now()
    activity = Activity(owner=author.email, created=now, **args)
    def txn():
      activity.put()
      activity.join(author, now)
    db.run_in_transaction(txn)
    
  def join(self, user, when=datetime.now()):
    w = when - self.created
    intW = w.days * 86400 + w.seconds
    joinRecord = Join(parent=self, key_name=user.email, weight=intW)
    joinRecord.put()
    

class Join(db.Model):
  weight = db.IntegerProperty(required = True)
  phone = db.StringProperty(required = True)
  car = db.StringProperty()
  comment = db.StringProperty()
    

class User(TipfyUser):
  firstName = db.StringProperty()
  lastName = db.StringProperty()
  dob = db.DateProperty()
  health = db.StringProperty()
  contactPhone = db.StringProperty()
  lastLogin = db.DateTimeProperty()
  
  def loggedIn(self):
    self.lastLogin = datetime.now()
    self.put()
  
  def screenName(self):
    return '%s %s' % (self.firstName, self.lastName)

class Address(db.Model):
  streetAddr = db.StringProperty(required = True)
  suburb = db.StringProperty(required = True)
  zipcode = db.StringProperty(required = True)
  state = db.StringProperty(required = True)
  country = db.StringProperty(required = True)
