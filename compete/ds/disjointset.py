from typing import Dict, Generic, Hashable, TypeVar

T = TypeVar('T', bound=Hashable)


class DisjointSet(Generic[T]):
    """
    A disjoint-set data structure (also called a union–find data structure or merge–find set) is a data structure
    that tracks a set of elements partitioned into a number of disjoint (non-overlapping) subsets.
    It provides near-constant-time operations (bounded by the inverse Ackermann function) to add new sets, to merge
    existing sets, and to determine whether elements are in the same set. In addition to many other uses,
    disjoint-sets play a key role in Kruskal's algorithm for finding the minimum spanning tree of a graph.
    https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    """
    __slots__ = ['_parents', '_sizes']

    def __init__(self) -> None:
        self._parents: Dict[T, T] = {}
        self._sizes: Dict[T, int] = {}

    def find(self, x: T) -> T:
        """
        Each "set" of items is identified by its "root" element. `find(x)` returns the identifier of the set
        in which `x` belongs.
        :param x: Item to find the set identifier of
        :return: Returns the element that identifies the set x belongs in
        """
        _parents = self._parents
        x, root = None, x  # iterate from x to the root to find the set's "identifier"
        while x != root:
            x, root = root, _parents.get(root, root)
        # note: this is NOT path-compression. This is "path-halving". It has the same worst-case complexity
        # as path-compression: https://en.wikipedia.org/wiki/Disjoint-set_data_structure#Path_splitting
        # It is both simpler to implement and works in a single iterative pass
        return root

    def size(self, x: T) -> int:
        """
        Given any item `x`, `size(x)` finds the size of the set (number of elements in the set) of items `x` belongs in
        :param x: Item belonging to a set
        :return: The size of the corresponding set
        """
        # remember to first find the root of the set, and then return the root's size
        return self._sizes.get(self.find(x), 1)

    def merge(self, x: T, y: T) -> None:
        """
        Given any two items, find the corresponding sets they belong to.
        If the items belong to different (disjoint) sets, merge the two sets into a larger set.
        If the items belong to the same set, do nothing.
        :param x: Any item belonging to any set
        :param y: Any item belonging to any set
        """
        x, y = self.find(x), self.find(y)  # remember, we must always merge the "roots" of each set
        if x == y:
            return  # if they already belong in the same set, do nothing
        size_x, size_y = self._sizes.get(x, 1), self._sizes.get(y, 1)
        if size_x < size_y:
            x, y = y, x  # the larger of the two sets will become parent.
            # This ensures a log(n) bound on tree height
        self._parents[y] = x
        self._sizes[x] = size_x + size_y  # remember to update the size of the new joint set
        self._sizes.pop(y, None)  # the previous "smaller" set doesn't not exist, so delete its size
