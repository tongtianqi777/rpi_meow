from flask import Flask, send_file
from db import DB
from flask_cors import CORS

from redis_handle import RedisHandle
from commons import LAST_TIME_SAW_CAT, SAW_CAT
from config import LAST_TIME_SAW_CAT_IMG

app = Flask(__name__)
CORS(app)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True
app.logger.disabled = True

redis_handle = RedisHandle()


@app.route('/last_time_saw_cat', methods=['GET'])
def get_last_time_saw_cat():
    val = redis_handle.get(LAST_TIME_SAW_CAT)
    return str(val) if val else ""


@app.route('/saw_cat', methods=['GET'])
def get_saw_cat():
    val = redis_handle.get(SAW_CAT)
    return str(val) if val else "false"


@app.route('/last_time_saw_cat_img', methods=['GET'])
def get_saw_cat():
    return send_file(LAST_TIME_SAW_CAT_IMG, mimetype='image/jpg')


@app.route('/get_event_log', methods=['GET'])
def get_saw_cat():
    db = DB()
    return db.get_all_event_history()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
