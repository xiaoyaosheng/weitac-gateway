#!/bin/sh
#chmod u+x trigger.sh
#nohup /weitac-gateway/trigger.sh > /weitac-gateway/trigger.date &
#if "$MIGRAGEDB" in "true"; then
#    /usr/bin/python /weitac-gateway/manage.py migrate --settings=weitac-gateway.settings
#fi

#/usr/local/bin/supervisord --nodaemon # Run supervisord in the foreground
python manage.py makemigrations
python manage.py migrate
nohup rabbitmq-server &
nohup python manage.py celery worker --loglevel=info --config=celeryconfig &
nohup python manage.py celery worker --loglevel=info --config=celeryconfig &
/usr/local/bin/supervisord --nodaemon
