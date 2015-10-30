#!/bin/sh
rev_path=`pwd`
config_path=`dirname ${rev_path}`/uwsgi
PYTHONPATH="${config_path}:${rev_path}" django-admin.py collectstatic --clear --noinput --settings settings_deploy
chmod +x ../uwsgi/post_deploy.sh
../uwsgi/post_deploy.sh