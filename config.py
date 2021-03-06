# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
  # Enable debugger. It will be loaded only in development.
  'middleware': [
    'tipfy.ext.debugger.DebuggerMiddleware',
  ],
  # Enable the UTSOAC application.
  'apps_installed': [
    'apps.utsoac',
  ],
}

config['tipfy.ext.session'] = {
  'secret_key': 'oops! that was lame :)',
  'default_backend': 'memcache',
  'max_age': 7 * 24 * 3600,
  'httponly': True,
}

config['tipfy.ext.auth'] = {
  'user_model': 'apps.utsoac.models.User',
}
