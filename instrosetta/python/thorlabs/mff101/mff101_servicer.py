import grpc
from enum import Enum
import pint
from instrosetta.interfaces.optomechanics import filter_flipper_pb2
from instrosetta.interfaces.optomechanics import filter_flipper_pb2_grpc
import mff101_device

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


class MFF101Servicer(filter_flipper_pb2_grpc.FilterFlipperServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = mff101_device.MFF101Device(*args, **kwargs)

    def Initialize(self, request, context):
        if self.device.connected:
            return filter_flipper_pb2.InitializeResponse(success=True)
        try:
            success=self.device.connect(request.serial_port)
            return filter_flipper_pb2.InitializeResponse(success=success)
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
            return filter_flipper_pb2.InitializeResponse(success=False)

    def Shutdown(self, request, context):
        if self.device.connected:
            return filter_flipper_pb2.ShutdownResponse(success=True)
        try:
            success=self.device.disconnect()
            return filter_flipper_pb2.ShutdownResponse(success=success)
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
            return filter_flipper_pb2.ShutdownResponse(success=False)
