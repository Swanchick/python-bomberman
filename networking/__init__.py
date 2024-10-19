from .client_network import ClientNetwork
from .server_network import ServerNetwork
from .network import BaseNetwork

NETWORK: BaseNetwork = None
from . import NETWORK
