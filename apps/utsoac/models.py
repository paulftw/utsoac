from google.appengine.ext import db

from datetime import datetime
import math
import os

from tipfy.ext.auth.model import User as TipfyUser

class User(TipfyUser):
  first_name = db.StringProperty()
  last_name = db.StringProperty()
  dob = db.DateProperty()
  health = db.StringProperty()
  contact_phone = db.StringProperty()
  last_login = db.DateTimeProperty(auto_now_add = True)
  
  def logged_in(self):
    self.last_login = datetime.now()
    self.put()
  
  def screen_name(self):
    return '%s %s' % (self.first_name, self.last_name)

class Address(db.Model):
  street_addr = db.StringProperty(required = True)
  suburb = db.StringProperty(required = True)
  zipcode = db.StringProperty(required = True)
  state = db.StringProperty(required = True)
  country = db.StringProperty(required = True)

class Activity(db.Model):
  owner = db.StringProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

  title = db.StringProperty(required = True)
  date = db.DateProperty(auto_now_add = True)
  description = db.TextProperty()
  participants = db.IntegerProperty(required = True)
  contact_phone = db.StringProperty()
  instructions = db.StringProperty()
  
  
  @classmethod
  def create(cls, author, **args):
    now = datetime.now()
    activity = Activity(owner=author.username, created=now, **args)
    def txn():
      activity.put()
      activity.join(author.username, phone=args['contact_phone'], when=now)
    db.run_in_transaction(txn)
    return activity
    
        
  def join(self, username, when=datetime.now(), **kwargs):
    w = Join.generate_weight(when - self.created)
    joinRecord = Join(parent=self, key_name=username, weight=w, **kwargs)
    joinRecord.put()
    return joinRecord
    
    
  @classmethod
  def get_by_key_encoded(cls, key_encoded):
    key = db.Key(key_encoded)
    activity = Activity.get(key)
    assert activity != None, 'Activity not found in db'
    return activity
    
  def get_joins(self):
    joins = Join.all().order('weight').ancestor(self).fetch(1000)
    return User.get_by_key_name([x.key().id_or_name() for x in joins])
    

class Join(db.Model):
  weight = db.IntegerProperty(required = True)
  phone = db.StringProperty(required = True)
  car = db.StringProperty()
  comments = db.StringProperty()
  gear = db.StringProperty()
  
  @classmethod
  def generate_weight(self, delta):
    secs = delta.days * 86400 + delta.seconds
    log = math.ceil(math.log(secs / 4.0 / 3600, 2))
    return log * 1000 + (ord(os.urandom(1)[0]) / 3)
    
