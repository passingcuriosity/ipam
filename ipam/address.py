"""
Represent and manipulate network ranges.
"""

from __future__ import annotations

from dataclasses import dataclass

def phex(value: int, width: int = 8) -> str:
    h = hex(value)[2:]
    return "0x" + h.rjust(width, "0")


@dataclass(frozen=True)
class Address:
    address: int
    prefix: int

    @property
    def network_mask(self: Address) -> int:
        return (0xFFFFFFFF << (32 - self.prefix)) & 0xFFFFFFFF

    @property
    def host_mask(self: Address) -> int:
        return (0xFFFFFFFF >> (32 - self.prefix)) & 0xFFFFFFFF

    @property
    def network(self: Address) -> int:
        return self.address & self.network_mask
    
    @property
    def host(self: Address) -> int:
        return self.address & self.host_mask

    def __post_init__(self: Address) -> None:
        if self.prefix < 0 or self.prefix > 32:
            raise ValueError(f"Invalid prefix '{self.prefix}': must be in 0-32")

    def __str__(self: Address):
        o1 = (self.address & 0xFF000000) >> 24
        o2 = (self.address & 0x00FF0000) >> 16
        o3 = (self.address & 0x0000FF00) >> 8
        o4 = self.address & 0x000000FF
        return f"{o1}.{o2}.{o3}.{o4}/{self.prefix}"
    
    def __lt__(self: Address, other: Address) -> bool:
        if not isinstance(other, Address):
            raise ValueError(f"Cannot compare Address to {type(other)}")
        
        return (self.network, self.prefix, self.host) < (other.network, other.prefix, other.host)
    
    def __contains__(self: Address, other: Address) -> bool:
        return (
            self.prefix <= other.prefix and
            self.network == (other.address & self.network_mask)
        )
    
    @classmethod
    def from_string(cls, value: str) -> Address:
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

    b = Address.from_string(f"192.168.256.150/17")
    print(f"{a} < {b} = {a < b}")
    print(f"{a} > {b} = {a > b}")
