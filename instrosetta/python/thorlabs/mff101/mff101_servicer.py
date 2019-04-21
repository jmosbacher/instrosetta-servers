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

    def bind(self, server):
        filter_flipper_pb2_grpc.add_FilterFlipperServicer_to_server(self, server)
        
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
        resp = filter_flipper_pb2.ShutdownResponse()
        try:
            self.device.disconnect()
            resp.success = True
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
            resp.success = False
        return resp

    def GetPosition(self, request, context):
        resp = filter_flipper_pb2.GetPositionResponse()
        try:
            resp.value = filter_flipper_pb2.FlipperPosition[self.device.position]
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to get position from device.')
        return resp

    def GetInfo(self, request, context):
        resp = filter_flipper_pb2.GetInfoResponse()
        try:
            resp.value = self.device.info
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to get position from device.')
        return resp

    def SetPosition(self, request, context):
        resp = filter_flipper_pb2.SetPositionResponse()
        try:
            self.device.sensors = request.value
            if request.validate:
                resp.value = self.device.sensors
            else:
                resp.value = request.value
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to set position.')
        return resp