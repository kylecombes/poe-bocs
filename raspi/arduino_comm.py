from serial import Serial
from threading import Thread
import json
from raspi.arduino_comm_event import ArduinoCommEvent

"""
This module handles all communication with an Arduino.
If communication with multiple Arduinos is needed, multiple ArduinoComm instances can be created.
"""


class ArduinoComm:

    thread = None

    """
    Creates a new instance of ArduinoComm.
    :param event_callback (function) a callback to use when something is received from the Arduino
    :param port (string) the serial port to connect to
    :param baudrate (int) the baudrate to use (defaults to 9600)
    """
    def __init__(self, event_callback, port='/dev/ttyACM0', baudrate=9600):
        self.event_callback = event_callback
        self.port = port
        self.baudrate = baudrate
        self.start_listening()

    def start_listening(self):
        self.thread = ArduinoCommThread(self.port, self.baudrate, self.event_callback)
        self.thread.setName('ArduinoCommThread for {}'.format(self.port))
        self.thread.start()

    def stop_listening(self):
        self.thread.stop()


class ArduinoCommThread(Thread):

    do_run = True

    def __init__(self, port, baudrate, event_callback):
        Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.event_callback = event_callback

    def run(self):
        cxn = Serial(self.port, baudrate=self.baudrate)

        while self.do_run:
            while cxn.inWaiting() < 1 and self.do_run:
                pass  # Might want to sleep here

            data = cxn.readline()
            if data:  # Make sure the data is valid before trying to parse it
                try:
                    data = data.decode('UTF-8')[0:-2]
                    self.process_event(data)
                except UnicodeDecodeError:
                    pass

    """
    Handles deserializing the event data and calling the event callback.
    """
    def process_event(self, raw_data):

        # Parse the JSON into a dictionary
        # try:
        raw_data = json.loads(raw_data)
        # except json.decoder.JSONDecodeError:
        #     return False

        # Check to make sure the necessary attributes are present
        if not raw_data:
            return False

        event_id = raw_data.get('event_id', None)
        if not event_id and event_id != 0:
            return False

        # Get the data, if there is any
        data = raw_data.get('data', None)

        # Get the options, if there are any
        options = raw_data.get('options', None)

        # Create an event object
        event = ArduinoCommEvent(event_id, data, options)

        # Pass the event to the callback
        self.event_callback(event)

    def stop(self):
        self.do_run = False