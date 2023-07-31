
from .types import AddressType, Network
from .tree import Tree


def prefix_error(network: Network):
    def fn(msg: str) -> str:
        return f"{network.location}: {network.address}: {msg}"
    return fn

def validate(networks: Tree[Network]) -> list[str]:
    """Check that forest of networks is complete and correct."""
    all_errors = []
    all_addresses = {}

    for network in networks:
        errors = []
        if network.address in all_addresses:
            original = all_addresses[network.address]
            errors.append(
                f"Duplicate definition, original at {original.location}"
            )
        else:
            all_addresses[network.address] = network
        if network.address_type == AddressType.host:
            if network.address.prefix < 32:
                errors.append("Host with network address")
        elif network.address_type == AddressType.subnet:
            if network.address.host:
                errors.append("Subnet with host bits set")
        elif network.address_type == AddressType.network:
            if network.address.host:
                errors.append("Network with host bits set")
        else:
            raise ValueError(f"Unhandled network type {network.address_type}")
        all_errors += map(prefix_error(network), errors)

    return all_errors
