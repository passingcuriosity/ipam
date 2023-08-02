
from .types import AddressType, Network
from .tree import Tree, TreeNode


def prefix_error(network: Network):
    def fn(msg: str) -> str:
        return f"{network.location}: {network.address}: {msg}"
    return fn


def validate(networks: Tree[Network]) -> list[str]:
    """Check that forest of networks is complete and correct."""
    all_errors = []
    all_addresses = {}

    for node in networks.nodes():
        errors = []
        network = node.value
        # Network ranges should be unique.
        if network.address in all_addresses:
            original = all_addresses[network.address]
            errors.append(
                f"Duplicate definition, original at {original.location}"
            )
        else:
            all_addresses[network.address] = network

        # Check all children are listed.
        errors += check_coverage(node)

        # Validate network range properties according to network type.
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


def check_coverage(node: TreeNode[Network]):
    errors = []

    network = node.value
    if node.children:
        children_size = sum(c.value.size for c in node.children)
        if network.size != children_size:
            type_name = network.address_type.value.capitalize()
            errors.append(
                f"{type_name} has {network.size} addresses but children only describe {children_size}"
            )

    return errors
