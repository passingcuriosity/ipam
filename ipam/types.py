
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from .address import Address


class AddressType(Enum):
    host = "host"
    network = "network"
    subnet = "subnet"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Loc:
    """Location in an input file or stream."""

    file: str
    line: int

    def __str__(self) -> str:
        return f"{self.file}:{self.line}"


@dataclass(frozen=True)
class Network:
    location: Loc
    address_type: AddressType
    address: Address
    comment: Optional[str] = None

    def __contains__(self: Network, other: Any) -> bool:
        return (
            isinstance(other, Network) and
            other.address in self.address
        )

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Network) and
            self.address == other.address
        )
    
    def __lt__(self, other: Any) -> bool:
        return (
            isinstance(other, Network) and
            self.address < other.address
        )

    def __str__(self) -> str:
        return f"{self.address_type} {str(self.address)}"
