
from instrosetta.interfaces.light_analysis import monochromator_pb2_grpc
from instrosetta.server import RpcServer
from .cm112_servicer import CM112Servicer
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CM112Server(RpcServer):
    
    servicer_class = CM112Servicer

if __name__ == '__main__':
    CM112Server().serve('[::]:50052')
