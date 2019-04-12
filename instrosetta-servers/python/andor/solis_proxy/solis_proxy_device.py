import serial
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


class SolisProxy:
    """
    Connects to a proxy script running in
    Andor solis, written with Andor BASIC.
    Script must be running for communication to work.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn = None
        self._sio = None
        self.polling_interval = 0.2

    @test_connection
    def read(self):
        msg = self._sio.readline().strip()
        self._conn.write(f"ACK:{msg}")
        return msg

    @test_connection
    def write(self, msg):
        self._sio.flush()
        self._sio.write(f'{msg}')
        time.sleep(0.1)
        resp = self._sio.readline().strip()
        if resp != f"ACK:{msg}":
            raise ConnectionError("Message not acknowledged by peer.")
        return True

    def read_response(self, timeout):
        responses = []
        start = time.time()
        while abs(time.time()-start)<timeout:
            resp = self.read()
            if resp == "OK":
                break
            elif resp != "":
                responses.append(resp)
            else:
                time.sleep(self.polling_interval)
        else:
            raise ConnectionError("Conversation not terminated by peer.")
        if len(responses)==1:
            return responses[0]
        else:
            return responses

    def query(self, *msgs, timeout=1):
        for msg in msgs:
            self.write(msg)
        resp = self.read_response(timeout)
        return resp
        
    def save(self, path):
        self.query("CALL","SAVE", path)

    def clear_screen(self):
        self.query("CALL","CLEARSCREEN")
        
    def get_shutter_state(self):
        return self.query("GET","SHUTTER")

    def set_shutter_state(self, state: ShutterState):
        self.query("SET","SHUTTER", state.value)

    def run(self):
        self.query('CALL","RUN')

    @property
    def grating(self):
        return self.query("GET","GRATING")

    @grating.setter
    def grating(self, value):
        if value in [1, 2]:
            self.query("SET","GRATING", value)
        while True:
            if self.grating == f"{value}":
                break
            else:
                time.sleep(4)

    @property
    def wavelength(self):
        return self.query("GET","WAVELENGTH")

    @wavelength.setter
    def wavelength(self, value):
        if (2000 >= value >= 200):
            self.query("SET","WAVELENGTH", value)

    @property
    def exposure(self):
        return self.query("GET","EXPOSURE")

    @exposure.setter
    def exposure(self, value):
        self.query("SET","EXPOSURE", value)

    @property
    def slit_width(self):
        return self.query("GET","SLIT_WIDTH")

    @slit_width.setter
    def slit_width(self, value):
        if (2500 >= value >=10):
            self.query("SET","SLIT_WIDTH", value)

    def connect(self, com_port, baudrate=115200, timeout=0.2):
        self.polling_interval = timeout
        self.disconnect()
        try:
            self._conn = serial.Serial(com_port, baudrate=baudrate, timeout=timeout)
            self._sio = io.TextIOWrapper(io.BufferedRWPair(self._conn, self._conn))
        except:
            pass

    @property
    def connected(self):
        if self._conn is None:
            return False
        return self._conn.is_open
        
    def disconnect(self):
        if self._connected:
            self._conn.close()
            