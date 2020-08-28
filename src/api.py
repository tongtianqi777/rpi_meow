from flask import Flask
from db import DB
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/latest_button_push', methods=['GET'])
def latest_button_push():
    db = DB()
    result = db.get_latest_button_push_ts()
    return result if result else ""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
