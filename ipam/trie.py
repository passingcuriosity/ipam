"""
A simple trie map with path compression.
"""

from __future__ import annotations

from typing import Generic, TypeVar

import logging


log = logging.getLogger(__name__)


T = TypeVar("T")


class TrieMap(Generic[T]):
    children: list[TrieMapNode[T]]

    def __init__(self) -> None:
        super().__init__()
        self.children = []

    def insert(self: TrieMap[T], value: T) -> None:
        return self.graft(TrieMapNode(value))
    
    def graft(self: TrieMap[T], other: TrieMapNode[T]) -> None:
        logging.debug(f"grafting {other} into {self}")
        idx = 0
        while idx < len(self.children):
            child = self.children[idx]
            logging.debug(f"children[{idx}] = {child}")
            if other.value in child.value:
                logging.debug(f"grafting into child {idx}")
                return child.graft(other)
            if child.value in other.value:
                other.graft(child)
                logging.debug(f"grafted child {idx} into {other}")
                del self.children[idx]
                continue
            if other.value < child.value:
                logging.debug(f"ignoring child {idx}: {child}")
                idx += 1
                continue
            else:
                self.children.insert(idx, other)
                return
        self.children.insert(idx, other)
        logging.debug(f"result {self}")

    def __repr__(self) -> str:
        return f"{self.children}"


class TrieMapNode(TrieMap):
    value: T
    children: list[TrieMapNode[T]]

    def __init__(self: TrieMapNode[T], value: T) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        if self.children:
            return f"({self.value}: {self.children})"
        else:
            return f"({self.value})"


if __name__ == "__main__":
    class S:
        def __init__(self, value):
            self.value = value
        
        def __contains__(self, other):
            return other.value.startswith(self.value)
        
        def __lt__(self, other):
            return self.value < other.value

        def __str__(self):
            return self.value

    data = "abc c abd a ab coffee c e d"

    t = TrieMap()
    print(t)
    for d in data.split():
        t.insert(S(d))
        print(t)
