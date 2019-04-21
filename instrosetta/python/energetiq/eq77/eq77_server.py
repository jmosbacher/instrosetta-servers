
from instrosetta.interfaces.light import light_source_pb2_grpc
from instrosetta.server import RpcServer
from eq77_servicer import EQ77Servicer
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class EQ77Server(RpcServer):
    servicer_class = EQ77Servicer

if __name__ == '__main__':
    EQ77Server().serve('[::]:50052')
