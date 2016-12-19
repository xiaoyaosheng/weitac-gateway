#!/bin/sh
#chmod u+x trigger.sh
#nohup /slark/trigger.sh > /slark/trigger.date &
if "$MIGRAGEDB" in "true"; then
    /usr/bin/python /slark/manage.py migrate --settings=event_server.settings
fi

/usr/local/bin/supervisord --nodaemon # Run supervisord in the foreground

