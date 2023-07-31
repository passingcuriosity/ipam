from ipam.address import Address


def test_contains_network_subnet():
    network = Address.from_string("1.2.0.0/16")
    subnet = Address.from_string("1.2.128.0/17")
    assert subnet in network
    assert network not in subnet


def test_contains_siblings():
    network = Address.from_string("1.2.0.0/16")
    subnet1 = Address.from_string("1.2.128.0/17")
    subnet2 = Address.from_string("1.2.0.0/17")
    assert subnet1 in network
    assert subnet2 in network
    assert subnet1 not in subnet2
    assert subnet2 not in subnet1


def test_example_1():
    a = Address.from_string("1.0.0.0/8")
    b = Address.from_string("1.128.0.0/9")

    assert a < b
    assert not b < a
    assert b in a


def test_example_2():
    a = Address.from_string("1.0.0.0/8")
    b = Address.from_string("2.0.0.0/8")

    assert a not in b
    assert b not in a


def test_example_3():
    a = Address.from_string("1.2.0.0/16")
    b = Address.from_string("1.3.0.0/16")

    assert a not in b
    assert b not in a

    assert a < b
    assert not b < a


def test_str():
    value = "1.2.3.4/32"
    assert value == str(Address.from_string(value))

