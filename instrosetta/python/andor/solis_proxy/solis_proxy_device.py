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


class SolisProxyDevice:
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
        self._sio.write(f'{msg}\n')
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
            if resp == "READY":
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

    def rpc(self, *msgs, timeout=2):
        for msg in msgs:
            self.write(msg)
        resp = self.read_response(timeout)
        return resp
        
    def save(self, path):
        self.rpc("CALL","SAVE", path)

    def clear_screen(self):
        self.rpc("CALL","CLEARSCREEN")
        
    @property
    def shutter(self):
        return self.rpc("GET","SHUTTER")

    @shutter.setter
    def shutter(self, state: ShutterState):
        self.rpc("SET","SHUTTER", state.value)

    def run(self):
        timeout = self.exposure + 5
        self.rpc('CALL","RUN', timeout=timeout)

    @property
    def grating(self):
        return self.rpc("GET","GRATING")

    @grating.setter
    def grating(self, value):
        if value in [1, 2]:
            self.rpc("SET","GRATING", value, timeout=100)

    @property
    def wavelength(self):
        return self.rpc("GET","WAVELENGTH")

    @wavelength.setter
    def wavelength(self, value):
        if (2000 >= value >= 200):
            self.rpc("SET","WAVELENGTH", value)

    @property
    def exposure(self):
        return self.rpc("GET","EXPOSURE")

    @exposure.setter
    def exposure(self, value):
        self.rpc("SET","EXPOSURE", value)

    @property
    def slit_width(self):
        return self.rpc("GET","SLIT_WIDTH")

    @slit_width.setter
    def slit_width(self, value):
        if (2500 >= value >=10):
            self.rpc("SET","SLIT_WIDTH", value)

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
        if self.connected:
            self._conn.close()