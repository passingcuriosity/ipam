"""Test network validation code."""


from ipam.address import Address
from ipam.tree import Tree
from ipam.types import Network, Loc, AddressType
from ipam.validation import validate


def test_validation_range_coverage():
    tree = Tree()
    tree.insert(
        Network(
            address_type=AddressType.network,
            address=Address.from_string("10.0.0.0/8"),
            location=Loc("<stdin>", 1),
        )
    )
    tree.insert(
        Network(
            address_type=AddressType.network,
            address=Address.from_string("10.0.0.0/9"),
            location=Loc("<stdin>", 2),
        )
    )
    assert len(validate(tree)) == 1

    tree.insert(
        Network(
            address_type=AddressType.network,
            address=Address.from_string("10.128.0.0/9"),
            location=Loc("<stdin>", 3),
        )
    )
    assert len(validate(tree)) == 0


def test_validation_duplicates():
    tree = Tree()
    tree.insert(
        Network(
            address_type=AddressType.network,
            address=Address.from_string("10.0.0.0/8"),
            location=Loc("<stdin>", 1),
        )
    )
    tree.insert(
        Network(
            address_type=AddressType.network,
            address=Address.from_string("10.0.0.0/9"),
            location=Loc("<stdin>", 2),
        )
    )
    tree.insert(
        Network(
            address_type=AddressType.network,
            address=Address.from_string("10.128.0.0/9"),
            location=Loc("<stdin>", 3),
        )
    )
    assert len(validate(tree)) == 0

    tree.insert(
        Network(
            address_type=AddressType.network,
            address=Address.from_string("10.0.0.0/9"),
            location=Loc("<stdin>", 4),
        )
    )
    assert len(validate(tree)) == 1
