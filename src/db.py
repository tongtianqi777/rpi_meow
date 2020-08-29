#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import pytz
import time
import sqlite3
from sqlite3 import Error
from config import *


def create_db_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

        return conn
    except Error as e:
        print("could not connect to DB: ", str(e))

    return conn


class DB(object):
    EVENT_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS meow_events (
    event text,
    timestamp text
);
"""

    def __init__(self):
        self.conn = create_db_connection(LOCAL_SQLITE_DB_FILE)
        self.run_query(DB.EVENT_TABLE_QUERY)

    def run_query(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()

            rows = c.fetchall()
            return rows
        except Error as e:
            print(e)

    def show_meta_table(self):
        self.conn()

    def add_button_push_event(self):
        now_ts = pytz.timezone("America/Los_Angeles").localize(datetime.now()).astimezone(pytz.utc).isoformat()

        query = """
INSERT INTO meow_events (event, timestamp)
VALUES ("meow_button_push", "{}"); 
""".format(now_ts)

        self.run_query(query)

    def get_latest_button_push_ts(self):
        query = """
SELECT
    timestamp
FROM
    meow_events
WHERE
    event = "meow_button_push"
ORDER BY
    timestamp DESC
LIMIT 1;
"""

        rows = self.run_query(query)
        if len(rows) == 0:
            return None
        return rows[0][0]


if __name__ == '__main__':
    # for dev only
    os.system("touch {}".format(LOCAL_SQLITE_DB_FILE))
    db = DB()
    time.sleep(2)
    db.add_button_push_event()
    print(db.get_latest_button_push_ts())
