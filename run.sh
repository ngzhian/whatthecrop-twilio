#!/bin/sh
# echo "------ Create database tables ------"
# python manage.py migrate --noinput
 
# echo "------ create default admin user ------"
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@myapp.local', 'Passw0rd')" | python manage.py shell
 
# echo "------ starting gunicorn &nbsp;------"
# gunicorn whatthecrop.wsgi --workers 2 -b 0.0.0.0:${VCAP_APP_PORT:=8000}
#!/bin/bash
if [ -z "$VCAP_APP_PORT" ];
then SERVER_PORT=8080;
else SERVER_PORT="$VCAP_APP_PORT";
fi
echo port is $SERVER_PORT
echo "------ Create database tables ------"
python manage.py migrate --noinput
python manage.py runserver --noreload 0.0.0.0:$SERVER_PORT
