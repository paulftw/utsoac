# -*- coding: utf-8 -*-

from tipfy import RequestHandler, Response
from tipfy.ext.jinja2 import render_response
from urls import navbar
from tipfy import (RequestHandler, RequestRedirect, Response, abort, cached_property, redirect, url_for)

from tipfy.ext.jinja2 import Jinja2Mixin
import forms
import simplejson

from models import Activity

from tipfy.ext.session import SessionMiddleware, SessionMixin, AllSessionMixins
from tipfy.ext.auth import MultiAuthMixin, login_required, user_required

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
    return self.render_response('activities.html', title='Upcoming Activities', activities=Activity.all())


class NewActivityHandler(BaseHandler):
  @user_required
  def get(self):
    return self.render_response('newactivity.html', title='New Activity', form=self.form)
  
  @user_required
  def post(self):
    if not self.form.validate():
      self.set_message('error', 'Invalid activity info. Please fix errors and try again.', life=None)
      return self.get()
    Activity.create(author=self.auth_current_user.username,
        title=self.form.title.data,
        description=self.form.description.data,
        date=self.form.date.data,
        participants=self.form.participants.data,
      )
    self.set_message('success', 'Great activity. Nice try!', life=None)
    return redirect('/')
    

  @cached_property
  def form(self):
    form = forms.NewActivityForm(self.request)
    form.contactPhone.data = self.auth_current_user.contactPhone
    return form
