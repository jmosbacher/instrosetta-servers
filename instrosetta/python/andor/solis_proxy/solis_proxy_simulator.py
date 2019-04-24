import struct
import time
import ast
import enum
from instrosetta.utils.devices import test_connection, TestableEnum


class ShutterState(TestableEnum):
    CLOSED = 0
    OPEN = 1
    AUTO = 2

class ReadoutMode(TestableEnum):
    FVB = 0
    MULTI_TRACK = 1
    RESERVED = 2
    SINGLE_TRACK = 3
    IMAGE = 4


class SolisProxyDeviceSimulator:
    """
    Simulates a proxy script running in
    Andor solis, written with Andor BASIC.
    
    """
    properties = ['exposure', 'wavelength', 'shutter', 'readout', 'grating', 'slit_width']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn = None
        self._sio = None
        self.polling_interval = 0.2
        self._values = {}
        self.connected = False
 
    def save(self, path):
        time.sleep(0.5)

    def clear_screen(self):
        time.sleep(0.5)

    def run(self):
        time.sleep(self.exposure+0.5)

    def connect(self,*args, **kwargs):
        self.connected = True
        
    def disconnect(self):
        self.connected = False

    def __getattr__(self, name):
        if name in self.properties:
            return self._values.get(name, 0)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self.properties:
            self._values[name] = value
            return
        return super().__setattr__(name, value)