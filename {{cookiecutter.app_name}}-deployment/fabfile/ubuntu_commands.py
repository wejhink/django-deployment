#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import run, cd

APT_GET_PACKAGES = [
    "build-essential",
    "git",
    "vim",
    "python-dev",
    "python-virtualenv",
    "python-pip",
    "libpq-dev",
    "postgresql",
    "postgresql-contrib",
    "nginx",
    "libxml2-dev",
    "libxslt1-dev",
    "lib32z1-dev",
    "libffi-dev", #Requirement of cffi
    "libssl-dev",
    "redis-server", #Using Redis as Django's session store and cache backend.
    "libtiff5-dev libjpeg8-dev libopenjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk",
    "elasticsearch"
]


def setup():
    "Install default packages for django"
    run("apt-get install " + " ".join(APT_GET_PACKAGES))


def setup_webserver():
    "Install default packages for django and NGINX"
    APT_GET_PACKAGES.append("nginx")
    setup()


def create_www():
    "Configure permissions on www"
    run("mkdir -p /www/")
    run("chown -R {{cookiecutter.ssh_user}}:www-data /www/")
    run("chmod 775 -R /www/")
    run("chmod g+s -R /www/")

def create_clone():
    with cd("/www/"):
        run("git clone git@bitbucket.org:{{cookiecutter.bitbucket_repository_user}}/{{cookiecutter.app_name}}.git")

def create_package(name):
    "Create virtualenv"
    create_www()
    package_name = "/www/%s-package" % str(name)
    run("virtualenv " + package_name)
    with cd(package_name):
        run("mkdir -p logs")
