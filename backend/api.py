import os
import uuid
import logging.config
from datetime import datetime

from celery import Celery
from flask import Flask, url_for, redirect, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('settings')
os.makedirs(app.config['DATA_DIR'], exist_ok=True)
logging.config.dictConfig(app.config['LOGGING_CONFIG'])
cors = CORS(app, resources={'*': {'origins': '*'}})
celery = Celery(app.import_name, config_source=app.config['CELERY_SETTINGS'])


@celery.task
def find_phonenumbers(self, picture_id):
    started = datetime.utcnow()
    # TODO: Do the picture processing here.
    elapsed = (datetime.utcnow() - started).total_seconds()
    return {'picture_id': picture_id, 'time_elapsed': elapsed}


@app.route('/result/<str:task_id>')
def get_result(task_id):
    task = celery.AsyncResult(task_id)
    result = task.result if task.ready() and task.successful() else None
    return jsonify(task_id=task.id, state=task.state, result=result)


@app.route('/start')
def start_task():
    picture_id = str(uuid.uuid4())
    assert len(request.files) == 1
    # TODO: Save picture to permanent database here.
    task = find_phonenumbers.apply_async((picture_id,), task_id=picture_id)
    assert task.id == picture_id
    return redirect(url_for('get_result', task_id=task.id))
