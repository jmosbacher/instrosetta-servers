import grpc
from enum import Enum
import pint
from instrosetta.interfaces.light_analysis import spectrograph_pb2
from instrosetta.interfaces.light_analysis import spectrograph_pb2_grpc
from instrosetta.servicer import GetterRPC, SetterRPC, simple_rpc
import solis_proxy_device
import solis_proxy_simulator


class SolisProxyServicer(spectrograph_pb2_grpc.SpectrographServicer):
    GetSlitWidth = GetterRPC(spectrograph_pb2.GetSlitWidthResponse, 'slit_width', value_name='magnitude')
    SetSlitWidth = SetterRPC(spectrograph_pb2.SetSlitWidthResponse, 'slit_width', value_name='magnitude')
    GetExposure = GetterRPC(spectrograph_pb2.GetExposureResponse, 'exposure', value_name='magnitude')
    SetExposure = SetterRPC(spectrograph_pb2.SetExposureResponse, 'exposure', value_name='magnitude')
    GetShutterState = GetterRPC(spectrograph_pb2.GetShutterStateResponse, 'shutter', value_name='magnitude')
    SetShutterState = SetterRPC(spectrograph_pb2.SetShutterStateResponse, 'shutter', value_name='magnitude')
    
    def bind(self, server):
        spectrograph_pb2_grpc.add_SpectrographServicer_to_server(self, server)
             
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = None

    @simple_rpc(spectrograph_pb2.InitializeResponse)
    def Initialize(self, request, response):
        if self.device:
            self.device.disconnect()
        if request.simulate:
            self.device = solis_proxy_simulator.SolisProxyDeviceSimulator()
            self.device.connect()
        else:
            self.device = solis_proxy_device.SolisProxyDevice()
            self.device.connect(request.serial_port, timeout=request.timeout,)
        response.success=True

    @simple_rpc(spectrograph_pb2.ShutdownResponse)
    def Shutdown(self, request, response):
        self.device.disconnect()
        response.success = True
    