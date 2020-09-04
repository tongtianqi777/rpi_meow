#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import pytz
import time
import sqlite3
from sqlite3 import Error
from config import *


def create_db_connections(db_file):
    """ create a 2 database connections (one in file, and another in memory) to SQLite database """
    file_conn = None
    memory_conn = None
    try:
        file_conn = sqlite3.connect(db_file)
        memory_conn = sqlite3.connect(":memory:")
        print(sqlite3.version)

        return file_conn, memory_conn
    except Error as e:
        print("could not connect to DB: ", str(e))

    return file_conn, memory_conn


class DB(object):
    # table in file
    EVENT_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS meow_events (
    event text,
    timestamp text
);
"""
    # table in memory
    BUTTON_PUSH_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS button_push (
    push_event text,
    timestamp text
);
"""
    # initial record for in-memory button push status
    INIT_BUTTON_PUSH_TABLE_QUERY = """
INSERT INTO button_push (push_event, timestamp)
VALUES ("latest_button_down", "{}"); 
"""

    def __init__(self):
        os.system("mkdir -p {}".format(os.path.dirname(LOCAL_SQLITE_DB_FILE)))
        os.system("touch {}".format(LOCAL_SQLITE_DB_FILE))  # create the db file if doesn't exist

        # get file and memory db connections
        self.file_conn, self.memory_conn = create_db_connections(LOCAL_SQLITE_DB_FILE)

        # create tables if not exist
        self.run_file_query(DB.EVENT_TABLE_QUERY)
        self.run_memory_query(DB.BUTTON_PUSH_TABLE_QUERY)

        # if there's record in file db, init the memory db with the latest push from file
        latest_push_ts_from_file = self.get_latest_button_push_ts(from_memory=False)
        if latest_push_ts_from_file:
            self.run_memory_query(DB.INIT_BUTTON_PUSH_TABLE_QUERY.format(latest_push_ts_from_file))
        else:
            self.run_memory_query(DB.INIT_BUTTON_PUSH_TABLE_QUERY.format(""))

    def run_file_query(self, sql):
        return self.run_query(self.file_conn, sql)

    def run_memory_query(self, sql):
        return self.run_query(self.memory_conn, sql)

    def run_query(self, conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()

            rows = c.fetchall()
            return rows
        except Error as e:
            print(e)

    def add_button_push_event(self):
        now_ts = pytz.timezone("America/Los_Angeles").localize(datetime.now()).astimezone(pytz.utc).isoformat()

        self.run_file_query("""
INSERT INTO meow_events (event, timestamp)
VALUES ("meow_button_push", "{}"); 
""".format(now_ts))

        self.run_memory_query("""
UPDATE button_push
SET timestamp = "{}"
WHERE
    push_event = "latest_button_down";
""".format(now_ts))

    def get_latest_button_push_ts(self, from_memory=True):
        if from_memory:
            rows = self.run_memory_query("""
SELECT
    timestamp
FROM
    button_push
WHERE
    push_event = "latest_button_down"
LIMIT 1;
""")
            if len(rows) == 0:
                return None
            return rows[0][0]

        else:
            rows = self.run_file_query("""
SELECT
    timestamp
FROM
    meow_events
WHERE
    event = "meow_button_push"
ORDER BY
    timestamp DESC
LIMIT 1;
""")
            if len(rows) == 0:
                return None
            return rows[0][0]


if __name__ == '__main__':
    # for dev only
    db = DB()
    time.sleep(2)
    db.add_button_push_event()
    print(db.get_latest_button_push_ts())
