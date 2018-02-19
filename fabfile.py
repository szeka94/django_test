import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/szeka94/django_test.git'
VIRTUALENV_PATH = '/home/ejoy/.virtualenvs/env/bin/'
workon = 'workon env && '

def deploy():
    site_folder = '/home/ejoy/django_test'  
    if not exists(site_folder):
    	run('mkdir -p {}'.format(site_folder))
    with cd(site_folder):  
        _get_latest_source()
        _update_virtualenv()
        _update_database()


def _get_latest_source():
    if exists('.git'):  
        run('git fetch')  
    else:
        run('git clone {} .'.format(REPO_URL))  
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run('git reset --hard {}'.format(current_commit))


def _update_virtualenv():
	run(workon + 'pip3.5 install -r requirements.txt', warn_only=True)

def _update_database():
    run(workon + 'python manage.py migrate')

def _update_translations():
    run(workon + 'python manage.py compilemessages')