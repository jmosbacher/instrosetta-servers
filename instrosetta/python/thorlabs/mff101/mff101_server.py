
from instrosetta.interfaces.optomechanics import filter_flipper_pb2_grpc
from instrosetta.server import RpcServer
from mff101_servicer import MFF101Servicer
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MFF101Server(RpcServer):
    @staticmethod
    def bind(sevicer, server):
        filter_flipper_pb2_grpc.add_FilterFlipperServicer_to_server(sevicer, server)
        
    servicer_class = MFF101Servicer

if __name__ == '__main__':
    MFF101Server().serve('[::]:50052')
