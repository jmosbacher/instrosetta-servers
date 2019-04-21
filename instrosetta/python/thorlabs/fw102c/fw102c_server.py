
from instrosetta.interfaces.optomechanics import filter_wheel_pb2_grpc
from instrosetta.server import RpcServer
from fw102c_servicer import FW102cServicer
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class FW102cServer(RpcServer):

    servicer_class = FW102cServicer

if __name__ == '__main__':
    FW102cServer().serve('[::]:50052')
