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
    #prepare_build(archive_file)
    #upload(archive_file)
    unpack(archive_file, env.version)
    update_virtualenv()
    migrate_schema()
    collect_static_files()
    reload_python_code()
    
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
        #sudo('rm %s' % archive_path)

def update_virtualenv():
    with cd(env.code_dir):
        sudo('source %s/bin/activate && pip install -r deploy/requirements.txt > /dev/null' % env.virtualenv)

def migrate_schema():
    with cd(env.code_dir):
        sudo('source %s/bin/activate && python manage.py migrate' % env.virtualenv)

def collect_static_files():
    with cd(env.code_dir):
        sudo('source %s/bin/activate && python manage.py collectstatic --noinput > /dev/null' % env.virtualenv)

def reload_python_code():
    with cd(env.builds_dir):
        sudo('touch %(build)s/%(wsgi)s' % env)




def old():
    # Upload and deploy    
    
    # Dependencies
    
    # Database, static, i18n

    # Server configuration
    deploy_apache_config()
    deploy_nginx_config()
    deploy_cronjobs()
    deploy_solr_schema()

    # Reload code
    nginx_reload()
    apache_reload()
    restart_celery_worker()
    restart_solr()
    
    # Clean up
    delete_old_builds()

def update_codebase(branch='master', repo='origin'):
    "Updates the codebase from the Git repo"
    print(green('Updating codebase from remote "%s", branch "%s"' % (repo, branch)))
    local('git checkout %s' % (branch))
    local('git pull %s %s' % (repo, branch))
    print(green('Pushing any local changes to remote "%s", branch "%s"' % (repo, branch)))
    local('git push %s %s' % (repo, branch))

def set_reference_to_deploy_from():
    # Versioning - we either deploy from a tag or we create a new one
    local('git fetch --tags')
    
    if env.build == 'dev':
        # Allow a new tag to be set, or generate one automatically
        create_tag = prompt('Tag this release? [y/N] ')
        if create_tag.lower() == 'y':
            print green("Showing latest tags for reference")
            local('git tag | sort -V | tail -5')
            env.version = prompt('Tag name [in format x.x.x]? ')
            # Sanity check tag
            if not re.match(r'^\d+\.\d+\.\d+$', env.version):
                raise RuntimeError("Tag name must in form x.x.x")
            print green("Tagging version %s" % env.version)
            local('git tag %s -m "Tagging version %s in fabfile"' % (env.version, env.version))
            print green("Pushing tags up to remote")
            local('git push --tags')
        else:
            # Use git describe to generate a build name for us
            env.version = local('git describe develop', capture=True).strip()
    else:
        # An existing tag must be specified to deploy to test or production
        local('git tag | sort -V | tail -5')
        env.version = prompt('Choose tag to build from: ')
        # Check this is valid
        print green("Checking chosen tag exists")
        local('git tag | grep "%s"' % env.version)
        
    if env.build == 'prod':
        # If a production build, then we ensure that the master branch
        # gets updated to include all work up to this tag
        local('git checkout master')
        local('git merge --no-ff %s' % env.version)

    print green("Building from version name %s" % env.version)




def deploy_apache_config():
    "Deploys the apache config"
    print green('Moving apache config into place')
    with cd(env.builds_dir):
        sudo('mv %(build)s/%(apache_conf)s /etc/apache2/sites-enabled/' % env)

def deploy_nginx_config():
    "Deploys the nginx config"
    print green('Moving nginx config into place')
    with cd(env.builds_dir):
        sudo('mv %(build)s/%(nginx_conf)s /etc/nginx/sites-enabled/' % env)

def deploy_cronjobs():
    "Deploys the cron jobs"
    print green('Deploying cronjobs')
    with cd(env.builds_dir):
        # Delete current cron jobs
        sudo("[ -f /etc/cron.d/%(project_code)s-%(build)s-* ] && rm /etc/cron.d/%(project_code)s-%(build)s-*" % env)
        
        # Replace variables in cron files
        sudo("rename 's#BUILD#%(build)s#' %(build)s/deploy/cron.d/*" % env)
        sudo("sed -i 's#VIRTUALENV_ROOT#%(virtualenv)s#' %(build)s/deploy/cron.d/*" % env)
        sudo("sed -i 's#BUILD_ROOT#%(code_dir)s#' %(build)s/deploy/cron.d/*" % env)
        sudo("mv %(build)s/deploy/cron.d/* /etc/cron.d" % env)

def deploy_solr_schema():
    "Deploys SOLR schema"
    print green('Deploying SOLR schema')
    with cd(env.builds_dir):
        sudo("mv -f %(build)s/deploy/solr/schema.xml /etc/solr/conf/" % env)


def restart_celery_worker():
    print green('Restarting celery worker')
    sudo('/etc/init.d/celeryd-%(build)s restart' % env)

def restart_solr():
    print green('Restarting Tomcat/SOLR')
    sudo('/etc/init.d/tomcat6 restart')

def delete_old_builds():
    print green('Deleting old builds')
    with cd(env.builds_dir):
        sudo('find . -maxdepth 1 -type d -name "%(build)s*" | sort -r | sed "1,3d" | xargs rm -rf' % env)

def apache_reload():
    "Reloads apache config"
    sudo('/etc/init.d/apache2 reload')

def apache_restart():
    "Restarts apache"
    sudo('/etc/init.d/apache2 restart')

def nginx_reload():
    "Reloads nginx config"
    sudo('/etc/init.d/nginx force-reload')

def nginx_restart():
    "Restarts nginx"
    sudo('/etc/init.d/nginx restart')

def apache_configtest():
    "Checks apache config syntax"
    sudo('/usr/sbin/apache2ctl configtest')

def nginx_configtest():
    "Checks nginx config syntax"
    sudo('/usr/sbin/nginx -t')

def provision():
    # Get details of provision
    client = prompt("Client name?")
    project_code = prompt("Project code?")
    ctx = {'client': client,
           'project_code': project_code}
    
    # Create base folder 
    base_folder = '/var/www/%(client)s/%(project_code)s/' % ctx
    sudo('[ ! -d %(folder)s ] && mkdir -p %(folder)s' % {'folder': base_folder})

    with cd(base_folder):
        # Create core folders
        folders = ['builds', 'media', 'virtualenvs', 'data', 'logs']
        environments = ['dev']
        for folder in folders:
            for environment in environments:
                sudo('[ ! -d %(folder)s/%(env)s ] && mkdir -p %(folder)s/%(env)s')

        # Create virtualenv
        for environment in environments:
            sudo('virtualenv --no-site-packages virtualenvs/%s' % environment)

