import itertools
import math

from ipam.tree import Tree
from ipam.address import Address


def test_tree_1():
    tree = Tree()

    tree.insert(Address.from_string("1.0.0.0/8"))
    assert str(tree) == "[1.0.0.0/8]"

    tree.insert(Address.from_string("1.2.0.0/16"))
    assert str(tree) == "[1.0.0.0/8:[1.2.0.0/16]]"

    tree.insert(Address.from_string("2.0.0.0/8"))
    assert str(tree) == "[1.0.0.0/8:[1.2.0.0/16], 2.0.0.0/8]"

    tree.insert(Address.from_string("1.0.0.0/8"))
    assert str(tree) == "[1.0.0.0/8:[1.0.0.0/8:[1.2.0.0/16]], 2.0.0.0/8]"

    tree.insert(Address.from_string("1.3.0.0/16"))
    assert str(tree) == "[1.0.0.0/8:[1.0.0.0/8:[1.2.0.0/16, 1.3.0.0/16]], 2.0.0.0/8]"


def test_insertion_order_invariant():
    addresses = [
        "1.3.0.0/16",
        "1.0.0.0/8",
        "1.2.3.0/24",
        "2.0.0.0/8",
        "1.0.0.0/24",
        "1.0.0.1/32",
    ]
    addresses = list(map(Address.from_string, addresses))
    trees = []

    for perm in itertools.permutations(addresses):
        tree = Tree()
        for a in perm:
            tree.insert(a)
        trees.append(str(tree))
    
    assert len(trees) == math.factorial(len(addresses))
    assert len(set(trees)) == 1


def test_iteration_values():
    addresses = [
        "1.0.0.0/8",
        "1.0.0.0/8",
        "1.2.0.0/16",
        "1.3.0.0/16",
        "2.0.0.0/8",
    ]

    tree = Tree()
    for a in addresses:
        tree.insert(Address.from_string(a))

    assert str(tree) == "[1.0.0.0/8:[1.0.0.0/8:[1.2.0.0/16, 1.3.0.0/16]], 2.0.0.0/8]"

    data = list(str(a) for a in iter(tree))
    assert data == addresses


def test_iteration_nodes():
    addresses = [
        "1.0.0.0/8",
        "1.0.0.0/8",
        "1.2.0.0/16",
        "1.3.0.0/16",
        "2.0.0.0/8",
    ]

    tree = Tree()
    for a in addresses:
        tree.insert(Address.from_string(a))

    assert str(tree) == "[1.0.0.0/8:[1.0.0.0/8:[1.2.0.0/16, 1.3.0.0/16]], 2.0.0.0/8]"

    data = list(str(node.value) for node in tree.nodes())
    assert data == addresses

