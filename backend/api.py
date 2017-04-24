import os
import uuid
import logging.config
import time
from datetime import datetime

from celery import Celery
from flask import Flask, redirect, request
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)
app.config.from_object('settings')

os.makedirs(app.config['DATA_DIR'], exist_ok=True)

logging.config.dictConfig(app.config['LOGGING'])
cors = CORS(app, resources={'*': {'origins': '*'}})
celery = Celery(app.import_name, config_source=app.config['CELERY_SETTINGS'])
api = Api(app)


@celery.task
def find_phonenumbers(picture_id):
    started = datetime.utcnow()
    # TODO: Do the picture processing here.
    time.sleep(10)
    elapsed = (datetime.utcnow() - started).total_seconds()
    return {
        'picture_id': picture_id,
        'picture_dimensions': (720, 1024),
        'processing_time': elapsed,
        'phone_numbers': [
            {
                'phone_number': '88001234567',
                'corner_upper_left': (126, 340),
                'corner_lower_right': (620, 1024),
            }
        ],
    }


@app.route('/tasks', methods=['POST'])
def start_task():
    picture_id = str(uuid.uuid4())
    assert len(request.files) == 1
    # TODO: Save picture to permanent database here.
    task = find_phonenumbers.apply_async((picture_id,), task_id=picture_id)
    assert task.id == picture_id
    return redirect(api.url_for(TaskResultAPI, task_id=task.id))


class TaskResultAPI(Resource):
    def get(self, task_id):
        task = celery.AsyncResult(task_id)
        result = task.result if task.ready() and task.successful() else {}
        return {'task_id': task.id, 'task_status': task.state,
                'task_result': result}


api.add_resource(TaskResultAPI, '/tasks/<task_id>')
