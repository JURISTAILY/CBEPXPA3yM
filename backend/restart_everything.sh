PROJECT="/var/www/callsense"
CELERY_LOG="$PROJECT/data/celery.log"

cd $PROJECT

chown -R www-data:www-data .

service uwsgi_callsense restart

ps auxww | grep 'celery worker' | grep $CELERY_LOG | grep -v grep | awk '{print $2}' | xargs -r kill -9
rm celeryd.pid
celery -A api.celery worker -D -l INFO -f $CELERY_LOG --uid=www-data
