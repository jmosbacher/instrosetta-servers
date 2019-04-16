import grpc
from enum import Enum
import pint
from instrosetta.interfaces.optomechanics import filter_wheel_pb2
from instrosetta.interfaces.optomechanics import filter_wheel_pb2_grpc
from .fw102c_device import FW102cDevice

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


class CM112Servicer(filter_wheel_pb2_grpc.MonochromatorServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = FW102cDevice(*args, **kwargs)

    def Initialize(self, request, context):
        if self.device.connected:
            return filter_wheel_pb2.InitializeResponse(success=True)
        try:
            self.device.connect(request.serial_port, baudrate=request.baudrate, timeout=request.timeout)
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
        return filter_wheel_pb2.InitializeResponse(success=True)

    def Shutdown(self, request, context):
        if self.device.connected:
            return filter_wheel_pb2.ShutdownResponse(success=True)
        try:
            self.device.disconnect()
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
        return filter_wheel_pb2.ShutdownResponse(success=True)
