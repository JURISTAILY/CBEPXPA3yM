import os
import logging.config

from celery import Celery
from flask import Flask, url_for, redirect, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('settings')
os.makedirs(app.config['DATA_DIR'], exist_ok=True)
logging.config.dictConfig(app.config['LOGGING_CONFIG'])
cors = CORS(app, resources={'*': {'origins': '*'}})
celery = Celery(app.import_name, config_source=app.config['CELERY_SETTINGS'])


@celery.task
def find_phonenumbers():
    raise NotImplementedError


@app.route('/result/<str:task_id>')
def get_result(task_id):
    result = celery.AsyncResult(task_id)
    if result.ready() and result.successful():
        data = result.result
    else:
        data = None
    return jsonify(task_id=task_id, status=result.state, result=data)


@app.route('/start')
def start_task():
    task = find_phonenumbers.delay()
    return redirect(url_for('get_result', task_id=task.id))
