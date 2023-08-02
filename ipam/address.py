"""
Represent and manipulate network ranges.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def phex(value: int, width: int = 8) -> str:
    h = hex(value)[2:]
    return "0x" + h.rjust(width, "0")


@dataclass(frozen=True)
class Address:
    address: int
    prefix: int

    def __post_init__(self: Address) -> None:
        if self.prefix < 0 or self.prefix > 32:
            raise ValueError(f"Invalid prefix '{self.prefix}': must be in 0-32")

    @property
    def network_mask(self: Address) -> int:
        return (0xFFFFFFFF << (32 - self.prefix)) & 0xFFFFFFFF

    @property
    def host_mask(self: Address) -> int:
        return (0xFFFFFFFF >> self.prefix) & 0xFFFFFFFF

    @property
    def network(self: Address) -> int:
        return self.address & self.network_mask

    @property
    def host(self: Address) -> int:
        return self.address & self.host_mask

    @property
    def size(self: Address) -> int:
        return 2 ** (32 - self.prefix)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self: Address):
        o1 = (self.address >> 24) & 0xFF
        o2 = (self.address >> 16) & 0xFF
        o3 = (self.address >> 8) & 0xFF
        o4 = self.address & 0xFF
        return f"{o1}.{o2}.{o3}.{o4}/{self.prefix}"

    def __contains__(self: Address, other: Any) -> bool:
        return (
            isinstance(other, Address) and
            self.prefix <= other.prefix and
            self.network == (other.address & self.network_mask) and
            self.host == 0
        )

    def __lt__(self: Address, other: Address) -> bool:
        if isinstance(other, Address):
            return (self.network, self.prefix, self.host) < (other.network, other.prefix, other.host)
        else:
            return False

    @classmethod
    def from_string(cls, value: str) -> Address:
        # TODO: Be defensive
        addr, prefix = value.split("/", maxsplit=1)
        o1, o2, o3, o4 = addr.split(".", maxsplit=3)
        ip = int(o1) << 24 | int(o2) << 16 | int(o3) << 8 | int(o4)
        p = int(prefix)
        return cls(ip, p)


if __name__ == "__main__":
    for p in range(8, 17):
        a = Address.from_string(f"192.168.256.150/{p}")
        print(a)
        print(f"network = {phex(a.network)} = {phex(a.address)} & {phex(a.network_mask)}")
        print(f"host    = {phex(a.host)} = {phex(a.address)} & {phex(a.host_mask)}")

    b = Address.from_string("192.168.256.150/17")
    print(f"{a} < {b} = {a < b}")
    print(f"{a} > {b} = {a > b}")
