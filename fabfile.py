import datetime
import os
import glob
import re

from fabric.api import local, run, sudo, env, settings
from fabric.colors import green, red, white, _wrap_with
from fabric.context_managers import cd, lcd
from fabric.operations import put, prompt

from fabconfig import *


def deploy():
    archive_file = '/tmp/build.tar.gz'
    prepare_build(archive_file)
    upload(archive_file)
    unpack(archive_file, env.version)
    update_virtualenv()
    migrate_schema()
    collect_static_files()
    deploy_apache_config()
    deploy_nginx_config()
    restart_services()
    reload_python_code()
    delete_old_builds()
    
def prepare_build(archive_file, reference='master'):
    local('git archive --format tar %s %s | gzip > %s' % (reference, env.web_dir, archive_file))

def upload(local_path):
    local('scp %s jupiter:/tmp' % local_path)

def unpack(archive_path, git_ref):
    now = datetime.datetime.now()
    env.build_dir = '%s-%s' % (env.build, now.strftime('%Y-%m-%d-%H-%M'))
    with cd(env.builds_dir):
        sudo('tar xzf %s' % archive_path)

        # Create new build folder
        sudo('if [ -d "%(build_dir)s" ]; then rm -rf "%(build_dir)s"; fi' % env)
        sudo('mv %(web_dir)s %(build_dir)s' % env)

        # Create new symlink
        sudo('if [ -h %(build)s ]; then unlink %(build)s; fi' % env)
        sudo('ln -s %(build_dir)s %(build)s' % env)

        # Remove archive
        sudo('rm %s' % archive_path)

def update_virtualenv():
    with cd(env.code_dir):
        sudo('source %s/bin/activate && pip install -r deploy/requirements.txt > /dev/null' % env.virtualenv)

def migrate_schema():
    with cd(env.code_dir):
        sudo('source %s/bin/activate && python manage.py syncdb > /dev/null' % env.virtualenv)
        sudo('source %s/bin/activate && python manage.py migrate > /dev/null' % env.virtualenv)

def collect_static_files():
    with cd(env.code_dir):
        sudo('source %s/bin/activate && python manage.py collectstatic --noinput > /dev/null' % env.virtualenv)

def reload_python_code():
    with cd(env.builds_dir):
        sudo('touch %(build)s/%(wsgi)s' % env)

def deploy_apache_config():
    with cd(env.builds_dir):
        sudo('mv %(build)s/%(apache_conf)s /etc/apache2/sites-enabled/' % env)

def deploy_nginx_config():
    with cd(env.builds_dir):
        sudo('mv %(build)s/%(nginx_conf)s /etc/nginx/sites-enabled/' % env)

def restart_services():
    sudo('/etc/init.d/apache2 restart')
    sudo('/etc/init.d/nginx restart')

def delete_old_builds():
    with cd(env.builds_dir):
        sudo('find . -maxdepth 1 -type d -name "%(build)s*" | sort -r | sed "1,3d" | xargs rm -rf' % env)
