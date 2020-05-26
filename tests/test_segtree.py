from functools import reduce

import pytest

from compete.ds.segtree import SegmentTree


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def xor(a, b):
    return a ^ b


def longest_common_prefix(a, b):
    result = []
    for x, y in zip(a, b):
        if x != y:
            break
        result.append(x)
    return ''.join(result)


operators = {
    int: [add, multiply, min, max, xor],
    str: [add, min, max, longest_common_prefix]
}

test_cases = {
    int: [10, -3, 2, 12, -13, 43, 7, 2, 13, -1],
    str: ['aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb']
}


def test_query_empty_tree():
    for data_type, ops in operators.items():
        for op in ops:
            tree = SegmentTree([], op)
            with pytest.raises(IndexError):
                tree.query(0)
            with pytest.raises(IndexError):
                tree.query(0, 10)


def test_query_single_index():
    for data_type, ops in operators.items():
        for op in ops:
            items = test_cases[data_type]
            tree = SegmentTree(items, op)
            for index, item in enumerate(items):
                assert tree.query(index) == item


def test_query_range():
    for data_type, ops in operators.items():
        for op in ops:
            items = test_cases[data_type]
            tree = SegmentTree(items, op)
            for start in range(len(items)):
                for end in range(start + 1, len(items) + 1):
                    expected = reduce(op, items[start: end])
                    actual = tree.query(start, end)
                    assert expected == actual

