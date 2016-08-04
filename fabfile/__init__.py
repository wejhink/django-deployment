#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from contextlib import contextmanager as _contextmanager

from fabric.api import run, env, run, cd, prefix, local
# extra content
from django_commands import *
from nginx_commands import *
from supervisor_commands import *
from ubuntu_commands import *



env.hosts = ['{{cookiecutter.server_ip}}']
env.user = 'root'
env.directory = '/www/{{cookiecutter.app_name}}/'
env.activate = 'source /www/{{cookiecutter.app_name}}-package/bin/activate'


@_contextmanager
def virtualenv():
    "Activate virtualenv"
    with cd(env.directory):
        with prefix(env.activate):
            yield


def py(context):
    "Execute python command"
    run("python " + context)


def info():
    "Show host name"
    run('uname -a')


def update():
    "Update server content"
    local("git push")
    with cd(env.directory):
        run('git fetch --all')
        run('git reset --hard origin/master')


def pip(*args):
    "Install package on server. Usage: pip:install,easy_thumbnails"
    with virtualenv():
        run("pip " + " ".join(args))


def load_requirements():
    "Install requirements packages"
    with cd(env.directory):
        with virtualenv():
            run("pip install -r requirements.txt")


def service(*args):
    "Control Services. Usage:start,nginx"
    run("service " + " ".join(args))


def omo():
    "Lava mais branco"
    with cd(env.directory):
        run('find -name "*.pyc" -delete')


def deploy():
    "Update git repository and reset nginx"
    update()
    omo()
    syncdb()
    static()
    supervisor_reset_gunicorn()
