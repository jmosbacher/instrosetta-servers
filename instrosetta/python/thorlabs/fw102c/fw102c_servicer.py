import grpc
from enum import Enum
import pint
from instrosetta.interfaces.optomechanics import filter_wheel_pb2
from instrosetta.interfaces.optomechanics import filter_wheel_pb2_grpc
import fw102c_device

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


class FW102cServicer(filter_wheel_pb2_grpc.FilterWheelServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = fw102c_device.FW102cDevice(*args, **kwargs)

    def Initialize(self, request, context):
        if self.device.connected:
            return filter_wheel_pb2.InitializeResponse(success=True)
        try:
            self.device.connect(request.serial_port, timeout=request.timeout)
            return filter_wheel_pb2.InitializeResponse(success=True)
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
            return filter_wheel_pb2.InitializeResponse(success=False)

    def Shutdown(self, request, context):
        if self.device.connected:
            return filter_wheel_pb2.ShutdownResponse(success=True)
        try:
            self.device.disconnect()
            return filter_wheel_pb2.ShutdownResponse(success=True)
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
            return filter_wheel_pb2.ShutdownResponse(success=False)
    
    