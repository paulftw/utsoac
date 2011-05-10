# -*- coding: utf-8 -*-

from tipfy import RequestHandler
from urls import navbar
from tipfy import (cached_property, redirect)

from tipfy.ext.jinja2 import Jinja2Mixin
import forms
import simplejson

from models import Activity, User

from tipfy.ext.session import SessionMiddleware, AllSessionMixins
from tipfy.ext.auth import MultiAuthMixin, user_required

class BaseHandler(RequestHandler, MultiAuthMixin, Jinja2Mixin, AllSessionMixins):
  middleware = [SessionMiddleware]
  
  def render_response(self, filename, **kwargs):
    auth_session = None
    if 'id' in self.auth_session:
      auth_session = self.auth_session

    self.request.context.update({
        'auth_session': auth_session,
        'current_user': self.auth_current_user,
        'login_url':    self.auth_login_url(),
        'logout_url':   self.auth_logout_url(),
        'current_url':  self.request.url,
        'pages': navbar,
        })
    if self.messages:
      self.request.context['messages'] = simplejson.dumps(self.messages)
    return super(BaseHandler, self).render_response(filename, **kwargs)

  def redirect_path(self, default='/'):
    if '_continue' in self.session:
      url = self.session.pop('_continue')
    else:
      url = self.request.args.get('continue', '/')
    if not url.startswith('/'):
      url = default
    return url


class MainPageHandler(BaseHandler):
  def get(self, **kwargs):
    return self.render_response('layout.html', title='UTS Outdoor Activities Club')

class ActivityListHandler(BaseHandler):
  def get(self, **kwargs):
    return self.render_response('activities.html', title='Upcoming Activities', 
        activities=Activity.all())


class NewActivityHandler(BaseHandler):
  @user_required
  def get(self):
    if self.activity != None:
      activity = self.activity
      if (self.auth_current_user.username == activity.owner):
        action = 'edit'
      else:
        action = 'view'
      self.form.process(obj=activity, activity_id=str(activity.key()))
      joined = activity.get_joins()
      
    else:
      action = 'new'
      activity = None
      joined = []

    return self.render_response('activity.html', title='%s Activity' % action, form=self.form, 
        activity=activity, action=action, participants=joined)
  
  @cached_property
  def activity(self):
    if self.request.args.has_key('activity'):
      return Activity.get_by_key_encoded(self.request.args.get('activity'))
    else:
      return None
      
  @user_required
  def post(self):
    if not self.form.validate():
      self.set_message('error', 'Invalid activity info. Please fix errors and try again.', 
          flash=True, life=10)
      return self.get()
    
    activity_id = self.form.activity_id.data
    if (activity_id != None and len(activity_id) > 0):
      activity = Activity.get_by_key_encoded(activity_id)
      # Check ownership
      if (activity.owner != self.auth_current_user.username):
        self.set_message('error', 'Post your own trip and edit it as much as you like!', 
                         life=10, flash=True)
        return redirect('/')
      else:
        activity
        # TODO copy form data to activity
    else:
      # New Activity
      activity = Activity.create(author=self.auth_current_user, **self.form.data)
      
    self.set_message('success', 'Activity saved. Let\'s do it!', flash=True, life=10)
    return redirect('/activity?activity=%s' % activity.key())


  @cached_property
  def form(self):
    form = forms.NewActivityForm(self.request)
    form.contact_phone.data = self.auth_current_user.contact_phone
    return form

class JoinActivityHandler(BaseHandler):
  @user_required
  def get(self):
    if not self.assert_activity_valid():
      return redirect('/')

    return self.render_response('joinactivity.html', title='Join Activity', 
        form=self.form,
        activity=self.activity,
        participants=self.participants, 
        leader=self.leader.screen_name())

  
  @cached_property
  def form(self):
    form = forms.JoinActivityForm(self.request)
    form.phone.data = self.auth_current_user.contact_phone
    if self.request.args.has_key('activity'):
      form.activity.data = self.request.args.get('activity')
    return form
  
  
  @cached_property
  def activity(self):
    return Activity.get_by_key_encoded(self.activity_id)
  
  
  @cached_property
  def leader(self):
    return User.get_by_username(self.activity.owner)
  
  
  @cached_property
  def activity_id(self):
    if self.request.args.has_key('activity'):
      return self.request.args.get('activity')
    else:
      return self.form.activity.data
    
    
  @cached_property
  def participants(self):
    return self.activity.get_joins()


  @user_required
  def post(self):
    if not self.assert_activity_valid():
      return redirect('/')

    if not self.form.validate():
      self.set_message('error', 'Invalid data entered. Please fix errors and try again.',
          flash=True, life=10)
      return self.get()
    
    if not self.form.weaver.data:
      self.set_message('error', 'We are sorry but due to the nature of this activity UTS OAC'
          ' is unable to eliminate all dangers.'
          ' Only people who accept the disclaimer are allowed to join.', life=10, flash=True)
      return self.get()
    
    kwargs = self.form.data
    if (self.form.car.data): 
      kwargs['car'] = 'yes'
    else:
      kwargs['car'] = ''
      
    self.activity.join(self.auth_current_user.username, **kwargs)
    self.set_message('success', 'You have signed up for %s!' % self.activity.title, life=5)
    return redirect('/')   


  def assert_activity_valid(self):
    try:
      assert self.activity != None
      assert self.leader != None
      assert self.participants != None
      return True
    except Exception, e:
      self.set_message('error', 'Unable to read activity %s: %s' % (self.activity_id, e), 
          flash=True, life=10)
      return False

