# "Inspired" by (stolen) some issue thread on github

import io,re,sys
import serial
from enum import Enum
import time
import logging
import ftd2xx
import ftd2xx.defines as constants
from instrosetta.utils.devices import test_connection

logger = logging.getLogger(__name__)


class Position(Enum):
    DOWN = down = d = D = b"\x6A\x04\x00\x02\x21\x01"
    UP = up = U = u = b"\x6A\x04\x00\x01\x21\x01"
    UNKNOWN = unknown = b''

class Status(Enum):
    down = b'*\x04\x06\x00\x81P\x01\x00\x02\x00\x00\x90'
    up = b'*\x04\x06\x00\x81P\x01\x00\x01\x00\x00\x90'
    moving_down = b'*\x04\x06\x00\x81P\x01\x00\x10\x00\x00\x90'
    moving_up = b'*\x04\x06\x00\x81P\x01\x00\x13\x00\x00\x90'
    query = b"\x29\x04\x00\x00\x21\x01"
    
class MFF101:
    device_props = ['position', 'info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._motor = None

    @property
    def connected(self):
        if self._motor is None:
            return False
        else:
            return True

    @property
    def position(self):
        if not self.connected:
            return 'UNKNOWN'
        self._motor.write(Status.query.value)
        mot_stat = self._motor.read(12)
        try:
            pos = Status(mot_stat).name
        except:
            pos = 'UNKNOWN'
        return pos

    @position.setter
    def position(self, pos):
        if pos in Position.__members__:
            cmd = Position[pos].value
            if cmd:
                self._motor.write(cmd)
                time.sleep(0.5)

    @property
    def info(self):
        return dict(self._motor.getDeviceInfo())

    def connect(self, port):
        motor = ftd2xx.openEx(port)
        motor.setBaudRate(115200)
        motor.setDataCharacteristics(constants.BITS_8, constants.STOP_BITS_1, constants.PARITY_NONE)
        time.sleep(.05)
        motor.purge()
        time.sleep(.05)
        motor.resetDevice()
        motor.setFlowControl(constants.FLOW_RTS_CTS, 0, 0)
        motor.setRts()
        self._motor = motor

    def disconnect(self):
        if self._motor is None:
            return 
        self._motor.close()
        self._motor = None
