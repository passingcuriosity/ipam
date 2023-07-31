import argparse
import logging
import sys

from .address import Address
from .tree import Tree
from .types import AddressType, Loc, Network
from .validation import validate


logger = logging.getLogger(__name__)


def read(file) -> list:
    """Read statements from an open file."""
    networks = []
    for (line, text) in enumerate(file):
        text = text.strip()
        if text.startswith("#"):
            continue
        if not text:
            continue
        parts = text.split(maxsplit=2)
        networks.append(
            Network(
                location=Loc(file=file.name, line=line),
                address_type=AddressType(parts[0]),
                address=Address.from_string(parts[1]),
                comment=parts[2] if len(parts) == 3 else None,
            )
        )
    return networks


parser = argparse.ArgumentParser()
parser.add_argument(
    "--verbose",
    "-v",
    action='count',
    default=0,
)
parser.add_argument(
    "FILES",
    nargs='+',
    type=argparse.FileType('r'),
    default=sys.stdin,
)


def main(argv: list[str]):
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.WARNING - (args.verbose * 10),
    )

    errors = []
    networks = Tree()

    for file in args.FILES:
        for addr in read(file):
            networks.insert(addr)
    
    logger.debug("Network tree: %s", networks)

    errors += validate(networks)

    logger.info(f"Processed: files={len(args.FILES)}; networks={len(networks)}; errors={len(errors)}")


    if errors:
        for error in sorted(errors):
            logger.error(error)
    else:
        for network in networks:
            logger.debug(str(network))
    
    exit(int(bool(errors)))
