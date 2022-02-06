#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import pytz
import sqlite3
from sqlite3 import Error
from config import *

EVENTS_HISTORY_TBL = "events_history"
MEM_CACHE_TBL = "mem_cache"


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
    # table in file (as permanent storage)
    EVENTS_HISTORY_TBL_DDL = f"""
CREATE TABLE IF NOT EXISTS {EVENTS_HISTORY_TBL} (
    event text,
    timestamp text
);
"""
    # table in memory (as memory cache)
    MEM_CACHE_TBL_DDL = f"""
CREATE TABLE IF NOT EXISTS {MEM_CACHE_TBL} (
    key text,
    val text
);
"""

    def __init__(self):
        os.system("mkdir -p {}".format(os.path.dirname(LOCAL_SQLITE_DB_FILE)))
        os.system("touch {}".format(LOCAL_SQLITE_DB_FILE))  # create the db file if doesn't exist

        # get file and memory db connections
        self.file_conn, self.memory_conn = create_db_connections(LOCAL_SQLITE_DB_FILE)

        # create tables if not exist
        self.run_file_query(DB.EVENTS_HISTORY_TBL_DDL)
        self.run_memory_query(DB.MEM_CACHE_TBL_DDL)

    def run_file_query(self, sql):
        return self._run_query(self.file_conn, sql)

    def run_memory_query(self, sql):
        return self._run_query(self.memory_conn, sql)

    def _run_query(self, conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()

            rows = c.fetchall()
            return rows
        except Error as e:
            print(e)

    def add_event_history(self, event: str, ts: str=None, timezone="America/Los_Angeles"):
        """
        add event to history using Los Angeles timezone as default
        :param event: event name
        :param ts: timestamp in ISO format. if not given the current time will be used.
        :param timezone: the name of timezone
        """
        ts_val = pytz.timezone(timezone).localize(datetime.now()).astimezone(pytz.utc).isoformat() if not ts else ts
        self.run_file_query(f"""
INSERT INTO {EVENTS_HISTORY_TBL} (event, timestamp)
VALUES ("{event}", "{ts_val}"); 
""")

    def update_mem_cache(self, key, val):
        self.run_memory_query(f"""
UPDATE {MEM_CACHE_TBL}
SET val = "{val}"
WHERE
    key = "{key}";
""")


if __name__ == '__main__':
    # for dev only
    db = DB()
    db.add_event_history('test')
