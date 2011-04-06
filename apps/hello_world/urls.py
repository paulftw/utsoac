# -*- coding: utf-8 -*-
from tipfy import Rule

navbar = [
  {'url':'', 'name':'home', 'handler':'MainPage'},
  {'url':'sandbox', 'name':'sandbox', 'handler':'Sandbox'},
  {'url':'activities', 'name':'activities', 'handler':'ActivityList'},
  {'url':'gallery', 'name':'photos', 'handler':'Gallery'},
  {'url':'join', 'name':'join club', 'handler':'JoinForm'},
  {'url':'contact', 'name':'contact\'em', 'handler':'Committee'},
  {'url':'about', 'name':'about this', 'handler':'StaticPage'},
]

def get_rules(app):
    """Returns a list of URL rules for the Hello, World! application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        Rule('/' + page['url'], endpoint='page' + page['url'], handler='apps.hello_world.handlers.' + page['handler'] + 'Handler')
        for page in navbar
        ]
    rules.extend([
        Rule('/auth/login', endpoint='auth/login', handler='apps.hello_world.utilhandlers.login.LoginHandler'),
        Rule('/auth/logout', endpoint='auth/logout', handler='apps.hello_world.utilhandlers.login.LogoutHandler'),
        Rule('/auth/signup', endpoint='auth/signup', handler='apps.hello_world.utilhandlers.login.SignupHandler'),
        Rule('/auth/register', endpoint='auth/register', handler='apps.hello_world.utilhandlers.login.RegisterHandler'),
        ])
        
    return rules
