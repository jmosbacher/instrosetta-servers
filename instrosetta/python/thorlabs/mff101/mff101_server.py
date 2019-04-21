
from instrosetta.server import RpcServer
from mff101_servicer import MFF101Servicer
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MFF101Server(RpcServer):

    servicer_class = MFF101Servicer

if __name__ == '__main__':
    MFF101Server().serve('[::]:50052')
