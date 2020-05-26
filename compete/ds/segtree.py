from typing import Callable, Generic, List, Optional, TypeVar

T = TypeVar('T')

sentinel = object()


def left_child(index: int) -> int:
    """returns the index of left child for the given index. Assumes 0 based indexing"""
    return 2 * index


def right_child(index: int) -> int:
    """returns the index of right child for the given index. Assumes 0 based indexing"""
    return 2 * index + 1


def is_left_child(index: int) -> bool:
    """check if the given index represents a left-child in the tree. Assumes 0 based indexing"""
    return index % 2 == 0


def is_right_child(index: int) -> bool:
    """check if the given index represents a right-child in the tree. Assumes 0 based indexing"""
    return index % 2 == 1


def parent(index: int) -> int:
    """returns the index of parent for the given index. Assumes 0 based indexing"""
    return index // 2


class SegmentTree(Generic[T]):
    """
    A segment tree, also known as a statistic tree, is a tree data structure used for storing information about
    intervals, or segments. It allows querying which of the stored segments contain a given point.
    It is, in principle, a static structure; that is, it's a structure that cannot be modified once it's built.

    Note: this implementation does NOT support range-updates. Use LazySegmentTree for that.
    Note: this implementation is based on https://codeforces.com/blog/entry/18051
    """
    __slots__ = ['_tree', '_func', '_n']

    def __init__(self, items: List[T], combinator: Callable[[T, T], T]) -> None:
        """
        :param items: The ordered list of items on which to form the Segment Tree
        :param combinator: A function that finds the value for a range, given values for two sub-ranges
        :type combinator: binary operator - takes two values and returns a single value
        """
        # note that this implementation takes 2*n space rather than 4*n
        # it builds the segment-tree in a bottom-up fashion, iteratively
        n = len(items)
        tree = [None] * (2 * n)  # preallocate space for efficiency
        for i, item in enumerate(items, start=n):
            tree[i] = item  # original data goes in the leaves
        for i in reversed(range(1, n)):  # form the intermediate nodes
            tree[i] = combinator(tree[left_child(i)], tree[right_child(i)])
        self._tree, self._func, self._n = tree, combinator, n

    def _combinator(self, left: T, right: T) -> T:
        if left is sentinel:
            return right
        if right is sentinel:
            return left
        return self._func(left, right)

    def query(self, start: int, end: Optional[int] = None) -> T:
        """
        Computes the value of  (a[start] (+) a[start+1] (+) ... a[end-1]), where (+) is the provided operation
        Note: The value returned is for range [start, end), i.e. including start but excluding end. This is
        to maintain idiomaticity with Python's `range(start, end)`
        """
        if end is None or end == start + 1:
            return self._tree[start + self._n]  # single index is being queried
        n, tree, combinator = self._n, self._tree, self._combinator
        # # start from the leaves
        # left_val, right_val = tree[start + n], tree[end + n - 1]
        # start, end = parent(start + n + 1), parent(end + n - 1)
        left_val, right_val = sentinel, sentinel
        start, end = start + n, end + n - 1
        while start <= end:  # this condition will become false when we reach the root
            if is_right_child(start):
                left_val = combinator(left_val, tree[start])
                start += 1
            if is_left_child(end):
                right_val = combinator(tree[end], right_val)
                end -= 1
            start, end = parent(start), parent(end)
        return combinator(left_val, right_val)

    def update(self, index: int, new_value: T) -> None:
        """
        Updates the value at given index, while maintaining the Segment Tree invariant
        :param index: the index of the element that should change
        :param new_value: new_value will replace any earlier value of the element
        """
        n, tree, combinator = self._n, self._tree, self._combinator
        index += n
        tree[index] = new_value
        while index > 1:
            index = parent(index)
            tree[index] = combinator(tree[left_child(index)], tree[right_child(index)])
