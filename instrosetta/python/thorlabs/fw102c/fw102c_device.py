import io
import re
import sys
import serial
import logging
from instrosetta.utils.devices import test_connection

logger = logging.getLogger(__name__)


class FW102C:
    device_props = ['speed', 'sensors', 'position']
    mappings = {'position':'pos'}

    regerr = re.compile("Command error.*")
    __doc__ = """
       Class to control the ThorLabs FW102C filter wheel
       
          fwl = FW102C()
          fwl.help()
          fw.connect(comport='COM1')
          fwl.position = 5
          fwl.position
          fwl.disconnect()

    """
    
    
    devInfo  = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ser = None
        self._sio = None
        self._status = {}
        self._filter_map = kwargs.get('filter_map', {})
    
    def help(self):
        print(self.__doc__)

    @property
    def connected(self):
        if self._ser is not None:
            return self._ser.is_open
        return False

    def connect(self, comport : str, timeout : float = 1):
        try:
            self._ser = serial.Serial(port=comport, baudrate=115200,
                                  bytesize=8, parity='N', stopbits=1,
                                  timeout=1, xonxoff=0, rtscts=0)
            self._sio = io.TextIOWrapper(io.BufferedRWPair(self._ser, self._ser, timeout),
                                         newline=None, encoding='ascii')
            self.devInfo = self.query('*idn?')

        except serial.SerialException as ex:
            print('Failed to connect to port {0}. Exception: {1}'.format(comport, ex))
            return

        except OSError as ex:
            print( 'Is port {0} available? Exception: {1}'.format(comport, ex))
            return
    
    def disconnect(self):
        self._sio.close()
        return True
    # end def disconnect

    def check_errors(self, msg):
        res = self.regerr.search(msg)
        if res:
            raise ConnectionError("Device returned errors: {errors}".format(res.group(0)))
    
    @test_connection
    def write(self, msg):
        self._sio.flush()
        success = self._sio.write(msg+'\r')
        if not success:
            raise ConnectionError("Cannot write to stream.")
        resp = self._sio.readline(2048).strip()
        self.check_errors(resp)
        if resp != msg:
            raise ConnectionError("Device not acknowledging message.")
        return True

    @test_connection
    def read(self):
        resp = self._sio.readline(2048).strip()
        self.check_errors(resp)
        return resp

    def get_prop(self, prop):
        name = self.mappings.get(prop, prop)
        self.write(name+'?')
        resp = self.read()
        try:
            val = ast.literal_eval(resp)
        except:
            val = resp
        return val

    def set_prop(self, prop, val):
        name = self.mappings.get(prop, prop)
        self.write("{}={}".format(name, val))
        val = getattr(self, prop)

    @property
    def info(self):        
        return self.devInfo

    @property
    def filter(self):
        pos = self.position
        return self._filter_map.get(pos, None)

    @filter.setter
    def filter(self, value):
        for pos, filter in self._filter_map.items():
            if filter == value:
                self.positon = pos

    def __setattr__(self, name, value):
        if name in self.device_props:
            name = self.mappings.get(name, name)
            self.set_prop(name, value)
        else:
            return super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.device_props:
            val = self.get_prop(name) 
            return val

        else:
            return super().__getattribute__(name)

    def __dir__(self):
        return super().__dir__() + self.device_props