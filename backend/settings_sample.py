from os.path import join, dirname, realpath

JSON_AS_ASCII = False

PROJECT_DIR = dirname(realpath(__file__))
DATA_DIR = join(PROJECT_DIR, 'data')

SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_SETTINGS = {
    'broker_url': 'amqp://guest:guest@localhost:5672//',
    'result_backend': 'db+' + SQLALCHEMY_DATABASE_URI,
    'task_track_started': True,
    'database_table_names': {
        'task': 'celery_taskmeta',
        'group': 'celery_groupmeta',
    },
}

LOGGER_NAME = 'autodial'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(levelname).1s] (%(name)s:%(lineno)d) %(message)s'
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(DATA_DIR, 'app.log'),
            'maxBytes': 5 * 1024000,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        LOGGER_NAME: {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
