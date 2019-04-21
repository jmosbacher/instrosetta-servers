import grpc
from enum import Enum
import pint
from instrosetta.interfaces.light_analysis import spectrograph_pb2
from instrosetta.interfaces.light_analysis import spectrograph_pb2_grpc
import solis_proxy_device

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


class SolisProxyServicer(spectrograph_pb2_grpc.SpectrographServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = None

    def bind(self, server):
        spectrograph_pb2_grpc.add_SpectrographServicer_to_server(self, server)

    def Initialize(self, request, context):
        resp = spectrograph_pb2.InitializeResponse()
        try:
            if self.device:
                self.device.disconnect()
            self.device = solis_proxy_device.SolisProxyDevice()
            self.device.connect(request.serial_port, timeout=request.timeout,)
            resp.success=True
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
            resp.success = False
        return resp

    def Shutdown(self, request, context):
        resp = spectrograph_pb2.ShutdownResponse()
        try:
            self.device.disconnect()
            resp.success = True
            
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to disconnect.')
            resp.success = False
        return resp
    