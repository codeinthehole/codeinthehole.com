import os
import sys
import site

sys.stdout = sys.stderr

# Project root
root = '/var/www/codeinthehole.com/builds/prod/'
sys.path.insert(0, root)

# Packages from virtualenv
activate_this = '/var/www/codeinthehole.com/virtualenvs/prod/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import newrelic.agent
newrelic.agent.initialize('/etc/newrelic/newrelic.ini')

# Set environmental variable for Django and fire WSGI handler 
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_CONF'] = 'conf.prod'
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

@newrelic.agent.wsgi_application()
def application(environ, start_response):
    return _application(environ, start_response)
