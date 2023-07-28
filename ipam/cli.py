from .address import Address
from .trie import TrieMap

def read(file) -> list:
    """Read statements from an open file."""
    data = []
    for line in file:
        line = line.strip()
        if line.startswith("#"):
            continue
        if not line:
            continue
        parts = line.split()
        if parts[0] == "host":
            data.append(Address.from_string(parts[1]))
        elif parts[0] == "subnet":
            data.append(Address.from_string(parts[1]))
        elif parts[0] == "network":
            data.append(Address.from_string(parts[1]))
        else:
            raise ValueError(f"Unknown statement '{parts[0]}': must be host, subnet, network")
    return data


def main(argv: list[str]):
    statements = []
    for fname in argv[1:]:
        with open(fname, "r") as f:
            statements += read(f)
    
    networks = TrieMap()
    for statement in sorted(statements):
        networks.insert(statement)
        print(statement)

    print(networks)
