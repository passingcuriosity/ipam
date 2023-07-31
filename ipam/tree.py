"""
A simple trie map with path compression.
"""

from __future__ import annotations

import itertools
import logging

from typing import Generic, Iterator, Protocol, TypeVar


log = logging.getLogger(__name__)


T = TypeVar("T")


class TreeValueProtocol(Protocol):
    def __lt__(self: T, other: T) -> bool: ...
    def __contains__(self: T, other: T) -> bool: ...


V = TypeVar("V", bound=TreeValueProtocol)


class Tree(Generic[V]):
    """
    Store values in sequence-prefix/set-covering relations.

    Kind of trie-ish except internal nodes which do not carry a value are
    omitted.

    This probably has a real name in CLRS, but I'd have to dig it out of my
    bookcase.

    The value type 'V' must implement `__lt__` for ordering and `__contains__`
    for the sequence-prefix/set-covering relation.

    E.g.
    
    > "a" in "ab"
    > "a" in "abcde"
    >
    > ["a":["ab":["abcde"]]]
    """

    children: list[TreeNode[V]]

    def __init__(self: Tree[V]) -> None:
        super().__init__()
        self.children = []

    def __iter__(self: Tree[V]) -> Iterator[V]:
        return itertools.chain(*self.children)
    
    def __len__(self: Tree[V]) -> int:
        return sum(map(len, self.children))

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self.children)) + "]"

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self.children)) + "]"

    def insert(
        self: Tree[V],
        value: V,
    ) -> None:
        """Insert a value into the tree."""
        node = TreeNode(value)
        return self.graft(node)
    
    def graft(
        self: Tree[V],
        other: TreeNode[V],
    ) -> None:
        """Graft a sub-tree into the tree."""
        idx = 0
        while idx < len(self.children):
            child = self.children[idx]
            if other.value in child.value:
                return child.graft(other)
            if child.value in other.value:
                other.graft(child)
                del self.children[idx]
                continue
            if not child.value < other.value:
                self.children.insert(idx, other)
                return
            idx += 1
        self.children.insert(idx, other)
        return


class TreeNode(Tree[V]):

    value: V
    children: list[TreeNode[V]]

    def __init__(
        self: TreeNode[V],
        value: V,
    ) -> None:
        super().__init__()
        self.value = value

    def __iter__(self: TreeNode[V]) -> Iterator[V]:
        return itertools.chain([self.value], *self.children)

    def __len__(self: Tree[V]) -> int:
        return 1 + sum(map(len, self.children))

    def __repr__(self: TreeNode[V]) -> str:
        if self.children:
            return f"{repr(self.value)}:{super().__repr__()})"
        else:
            return repr(self.value)
        
    def __str__(self: TreeNode[V]) -> str:
        if self.children:
            return f"{str(self.value)}:{super().__str__()}"
        else:
            return str(self.value)


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

    t = Tree[S]()
    for d in data.split():
        t.insert(S(d))
        print(t)
