import os
import platform

if platform.system() == 'Darwin':
    LOCAL_SQLITE_DB_FILE = "/Users/tianqitong/tmp/rpi_meow/rpi_meow.db"
    LAST_TIME_SAW_CAT_IMG = "/Users/tianqitong/tmp/rpi_meow/last_time_saw_cat.jpg"

elif platform.system() == 'Linux':
    LOCAL_SQLITE_DB_FILE = "/home/pi/dev/rpi_meow/rpi_meow.db"
    LAST_TIME_SAW_CAT_IMG = "/home/pi/dev/rpi_meow/last_time_saw_cat.jpg"
