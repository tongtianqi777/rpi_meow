from flask import Flask
from db import DB

app = Flask(__name__)


@app.route('/latest_button_push', methods=['GET'])
def latest_button_push():
    db = DB()
    return db.get_latest_button_push_ts()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
