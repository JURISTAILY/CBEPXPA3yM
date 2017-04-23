PROJECT=/var/www/callsense
USER=www-data

cd $PROJECT

chown -R $USER:$USER .

service uwsgi_callsense restart
service nginx reload

ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs -r kill -9
rm celeryd.pid
celery -A api.celery worker -D -l INFO -f $PROJECT/data/celery.log --uid=$USER
