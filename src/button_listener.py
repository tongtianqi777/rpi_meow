#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import RPi.GPIO as GPIO
import time

from db import DB

ledPin = 11
buttonPin = 12


class ButtonListener(object):
    def __init__(self):
        self.db = DB()

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(ledPin, GPIO.OUT)
        GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # pull up input mode

    def loop(self):
        while True:
            if GPIO.input(buttonPin) == GPIO.LOW:  # button down
                # turn on the led for 2 seconds
                GPIO.output(ledPin, GPIO.HIGH)
                self.db.add_button_push_event()
                time.sleep(5)
                GPIO.output(ledPin, GPIO.LOW)

    def destroy(self):
        GPIO.cleanup()


if __name__ == '__main__':
    print("starting button listener...")
    button_listener = ButtonListener()
    button_listener.setup()
    try:
        button_listener.loop()
    except KeyboardInterrupt:
        button_listener.destroy()
