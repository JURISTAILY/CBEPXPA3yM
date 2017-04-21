# Commands

    sudo apt-get install rabbitmq-server
    sudo service rabbitmq-server status

    service uwsgi_autodial restart
    celery -A api.celery worker -D -l INFO -f /var/www/autodial/data/celery.log --uid=www-data
    ps auxww | grep 'celery worker'
    pkill -9 -f 'celery worker'; rm celeryd.pid
