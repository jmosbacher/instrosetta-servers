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
        self.device = None

    def Initialize(self, request, context):
        if self.device and self.device.connected:
            return filter_wheel_pb2.InitializeResponse(success=True)
        try:
            self.device = fw102c_device.FW102cDevice(filter_map=request.filter_map)
            self.device.connect(request.serial_port, timeout=request.timeout,)
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
    
    def GetPositionOptions(self, request, context):
        resp = filter_wheel_pb2.GetPositionOptionsResponse()
        try:
            resp.options = self.device.filter_options
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to get options from device.')
        return resp
   
    
    def GetPosition(self, request, context):
        resp = filter_wheel_pb2.GetPositionResponse()
        try:
            resp.value = self.device.position
            
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to get position from device.')
        return resp

    def SetPosition(self, request, context):
        resp = filter_wheel_pb2.SetPositionResponse()
        try:
            self.device.position = request.value
            if request.validate:
                resp.value = self.device.position
            else:
                resp.value = request.value
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to set position.')
        return resp

    def GetFilterOptions(self, request, context):
        resp = filter_wheel_pb2.GetFilterOptionsResponse()
        try:
            resp.options = self.device.filter_options.items()
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to get options from device.')
        return resp

    def GetFilter(self, request, context):
        return super().GetFilter(request, context)

    def GetSensorsOptions(self, request, context):
        resp = filter_wheel_pb2.GetSensorsOptionsResponse()
        try:
            resp.options = self.device.sensors_options
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to get options from device.')
        return resp

    def GetSensors(self, request, context):
        resp = filter_wheel_pb2.GetSensorsResponse()
        try:
            resp.value = self.device.sensors
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to get position from device.')
        return resp
    
    def SetSensors(self, request, context):
        resp = filter_wheel_pb2.SetSensorsResponse()
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

    