import serial
import struct
import time

class CM112Device:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    @staticmethod
    def wl_to_bytes(wl):
        a = wl*10.
        high = int(a/256)
        low = int(a - high*256)
        return high, low

    @staticmethod
    def encode(*args):
        return b''.join([struct.pack('B', arg) for arg in args])

    def query(self, *args):
        msg = self.encode(*args)
        self.conn.write(msg)
        return list(self.conn.read(2048))
    
    def home(self):
        self.query(255,255,255)
    
    @property
    def wavelength(self):
        h, l, *_ = self.query(56, 0)
        return (h*256+l)/10

    @wavelength.setter 
    def wavelength(self, wl):
        high, low = self.wl_to_bytes(wl)  #Set monochromator to wl
        while True:
            cwl = self.wavelength
            if abs(wl - cwl)<1:
                break
            else:
                self.query(16, high, low)
                time.sleep(0.1)
                
    @property
    def grating(self):
        h,l, *_ = self.query(56, 4)
        return l

    @grating.setter
    def grating(self, gr):
        if gr not in [1,2]:
            return
        self.query(26, gr)
        while True:
            try:
                if self.grating==gr:
                    break
                time.sleep(2)
            except:
                pass
            
    def connect(self, port, baudrate=9600, timeout=1):
        self.conn = serial.Serial(port, baudrate=baudrate, timeout=timeout)


    @property
    def connected(self):
        if self.conn is None:
            return False
        return self.conn.is_open
        

    def disconnect(self):
        if self.connected:
            self.conn.close()


