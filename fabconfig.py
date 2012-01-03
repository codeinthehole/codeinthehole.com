from fabric.api import env

env.builds_dir = '/var/www/codeinthehole.com/builds'
env.web_dir = 'www'

def prod():
    env.build = 'prod'
    env.hosts = ['96.126.98.110:31245']
    env.user = 'david'
    env.virtualenv = '/var/www/codeinthehole.com/virtualenvs/prod'
    env.code_dir = '/var/www/codeinthehole.com/builds/prod'
    env.apache_conf = 'deploy/apache/codeinthehole'
    env.nginx_conf = 'deploy/nginx/codeinthehole'
    env.wsgi = 'deploy/wsgi/prod.wsgi'

