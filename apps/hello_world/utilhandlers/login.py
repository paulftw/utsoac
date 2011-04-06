# -*- coding: utf-8 -*-

from tipfy import RequestHandler, Response
from tipfy.ext.jinja2 import render_response
from tipfy import (cached_property, redirect, url_for)

import apps.hello_world.forms as forms
import simplejson

from apps.hello_world.handlers import BaseHandler
from tipfy.ext.auth import login_required, user_required

# Login stuff

class LoginHandler(BaseHandler):
    def get(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't display the signup form.
            return redirect(redirect_url)

        opts = {'continue': self.redirect_path()}
        context = {
            'form': self.form,
        }
        return self.render_response('login.html', **context)

    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't display the signup form.
            return redirect(redirect_url)

        if self.form.validate():
            username = self.form.loginid.data
            password = self.form.password.data
            remember = self.form.remember.data

            res = self.auth_login_with_form(username, password, remember)
            if res:
                return redirect(redirect_url)
        # Did not recognize password or whatever.
        self.set_message('error', 'Authentication failed. Please try again.',
            life=None)
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return forms.LoginForm(self.request)


class LogoutHandler(BaseHandler):
    def get(self, **kwargs):
        self.auth_logout()
        return redirect(self.redirect_path())


class SignupHandler(BaseHandler):
    @login_required
    def get(self, **kwargs):
        if self.auth_current_user:
            # User is already registered, so don't display the signup form.
            return redirect(self.redirect_path())

        return self.render_response('signup.html', form=self.form)

    @login_required
    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't process the signup form.
            return redirect(redirect_url)

        if self.form.validate():
            auth_id = self.auth_session.get('id')
            user = self.auth_create_user(self.form.nickname.data, auth_id)
            if user:
                self.auth_set_session(user.auth_id, user.session_id, '1')
                self.set_message('success', 'You are now registered. '
                    'Welcome!', flash=True, life=5)
                return redirect(redirect_url)
            else:
                self.set_message('error', 'This nickname is already '
                    'registered.', life=None)
                return self.get(**kwargs)

        self.set_message('error', 'A problem occurred. Please correct the '
            'errors listed in the form.', life=None)
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return SignupForm(self.request)


class RegisterHandler(BaseHandler):
    def get(self, **kwargs):
        redirect_url = self.redirect_path()
        if self.auth_current_user:
            # User is already registered, so don't display the registration form.
            return redirect(redirect_url)

        return self.render_response('register.html', form=self.form)

    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't process the signup form.
            return redirect(redirect_url)

        if self.form.validate():
            username = self.form.loginid.data
            password = self.form.password.data
            password_confirm = self.form.password_confirm.data

            if password != password_confirm:
                self.set_message('error', "Password confirmation didn't match.",
                    life=None)
                return self.get(**kwargs)

            auth_id = 'own|%s' % username
            user = self.auth_create_user(username, auth_id, password=password)
            if user:
                self.auth_set_session(user.auth_id, user.session_id, '1')
                self.set_message('success', 'You are now registered. '
                    'Welcome!', flash=True, life=5)
                return redirect(redirect_url)
            else:
                self.set_message('error', 'This nickname is already '
                    'registered.', life=None)
                return self.get(**kwargs)

        self.set_message('error', 'A problem occurred. Please correct the '
            'errors listed in the form.', life=None)
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return forms.RegistrationForm(self.request)
