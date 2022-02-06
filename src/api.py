import argparse
import json

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


@app.route('/last_time_saw_cat_ts', methods=['GET'])
def get_last_time_saw_cat_ts():
    val = redis_handle.get(LAST_TIME_SAW_CAT)
    return str(val) if val else ""


@app.route('/saw_cat', methods=['GET'])
def get_saw_cat():
    val = redis_handle.get(SAW_CAT)
    return str(val) if val else "false"


@app.route('/last_time_saw_cat_img', methods=['GET'])
def get_last_time_saw_cat_img():
    return send_file(LAST_TIME_SAW_CAT_IMG, mimetype='image/jpg')


@app.route('/event_log', methods=['GET'])
def get_event_log():
    db = DB()
    return json.dumps(db.get_all_event_history())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--port',
        help='Port for API service',
        required=False,
        default=5000)
    args = parser.parse_args()

    # for MacOS the port cannot be 5000, because it's being used by default
    # do: python api.py --port 5001
    app.run(debug=True, host='0.0.0.0', port=args.port)
