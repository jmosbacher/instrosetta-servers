import grpc
from enum import Enum
import pint
from instrosetta.interfaces.light_analysis import monochromator_pb2 as pb2
from instrosetta.interfaces.light_analysis import monochromator_pb2_grpc as pb2_grpc
from .cm112_device import CM112Device

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


class CM112Servicer(pb2_grpc.MonochromatorServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = CM112Device(*args, **kwargs)

    def Connect(self, request, context):
        if self.device.connected:
            return pb2.ConnectResponse()
        try:
            self.device.connect(request.serial_port, baudrate=request.baudrate, timeout=request.timeout)
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
        return pb2.ConnectResponse()

    def GetWavelengthRange(self, request, context):
        resp = pb2.GetWavelengthRangeResponse()
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            resp = pb2.GetWavelengthRangeResponse(
                minimum = 200,
                maximum = 2000,
                units = "nm",
            )
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp

    def GetWavelength(self, request, context):
        resp = pb2.GetWavelengthResponse()
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            resp = pb2.GetWavelengthResponse(
                wavelength = self.device.wavelength,
                units = "nm"
            )
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp

    def SetWavelength(self, request, context):
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        resp = pb2.SetWavelengthResponse()
        try:
            self.device.wavelength = Q_(request.wavelenth, request.units).to(ureg.nanometer)
            resp =  pb2.SetWavelengthResponse(
                wavelength = self.device.wavelength,
                units = "nm"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')

        return resp

    def GetGratingOptions(self, request, context):
        resp = pb2.GetGratingOptionsResponse()
        
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            resp = pb2.GetGratingOptionsResponse(
                options = (1,2),
            )
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp

    def GetGrating(self, request, context):
        resp = pb2.GetGratingResponse()
        
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            resp = pb2.GetGratingResponse(
                grating = self.device.grating,
            )
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp

    def SetGrating(self, request, context):
        resp = pb2.SetGratingResponse()
        
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            self.device.grating = request.grating
            resp = pb2.SetGratingResponse(
                grating = self.device.grating,
            )
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp