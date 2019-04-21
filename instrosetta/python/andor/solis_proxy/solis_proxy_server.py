
from instrosetta.server import RpcServer
from solis_proxy_servicer import SolisProxyServicer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class SolisProxyServer(RpcServer):
    servicer_class = SolisProxyServicer

if __name__ == '__main__':
    SolisProxyServer().serve('[::]:50052')
