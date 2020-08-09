#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
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

    def __init__(self, db_file):
        self.conn = create_db_connection(db_file)
        self.run_query(DB.EVENT_TABLE_QUERY)

    def run_query(self, sql):
        try:
            print("[QUERY] {}".format(sql))
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Error as e:
            print(e)

    def show_meta_table(self):
        self.conn()

    def add_button_push_event(self):
        now_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = """
INSERT INTO meow_events (event, timestamp)
VALUES ("meow_button_push", "{}"); 
""".format(now_ts)

        self.run_query(query)


if __name__ == '__main__':
    # for dev only
    os.system("touch {}".format(LOCAL_SQLITE_DB_FILE))
    db = DB(LOCAL_SQLITE_DB_FILE)
    db.add_button_push_event()
    time.sleep(3)
    db.add_button_push_event()
