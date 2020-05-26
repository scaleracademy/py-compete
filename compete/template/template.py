def solve(test_case):
    pass


MOD = 10 ** 9 + 7


class Config:
    has_tests = False
    debug = False
    print_recursion = False
    prime_sieve = 1


# =================================================================================================================
#                                                  T E M P L A T E
# =================================================================================================================

from collections import Counter, defaultdict, deque, namedtuple
from functools import reduce
from heapq import heapify, heappop, heappush, heappushpop, heapreplace, merge, nlargest, nsmallest
from itertools import accumulate, chain, combinations, combinations_with_replacement, count, cycle, permutations
from math import *


def dp(f):
    cache = {}

    def g(*args):
        args = tuple(args)
        if args in cache:
            return cache[args]
        x = f(*args)
        cache[args] = x
        return x

    return g


def trie():
    return defaultdict(trie)


def _():
    print(heapify, heappop, heappush, heappushpop, heapreplace, merge, nlargest, nsmallest)
    print(namedtuple, deque, Counter, defaultdict)
    print(accumulate, permutations, combinations, combinations_with_replacement, chain, cycle, count)
    print(reduce)
    print(inf)


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n <= Config.prime_sieve:
        return spf[n] == n
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def prime_factorize(n):
    if n <= 3:
        return [(n, 1)]
    factorization = []
    f = 2
    while f * f <= n > Config.prime_sieve:
        p = 0
        while n % f == 0:
            p += 1
            n //= f
        factorization.append((f, p))
        f += 1
    while 1 < n != spf[n]:
        p = 0
        f = spf[n]
        while n % f == 0:
            n //= f
            p += 1
        factorization.append((f, p))
    if n > 1:
        factorization.append((n, 1))
    return factorization


def count_factors(factorization, mod=None):
    ans = 1
    for f, p in factorization:
        ans *= 1 + p
        if mod is not None:
            ans %= mod
    return ans


def sum_of_factors(n, mod=None):
    pass


def ncr(n, r, mod=None):
    pass


def pow(n, p, mod=None):
    ans = 1
    while p > 0:
        if p % 2 == 1:
            ans *= n
            if mod is not None:
                ans %= mod
        n *= n
        if mod is not None:
            n %= mod
        p //= 2
    return ans


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def x_gcd(a, b):
    """:return: (g, x, y) where ax + my = g = gcd(a, b)"""
    px, x = 1, 0
    py, y = 0, 1
    while b:
        q = a // b
        x, px = px - q * x, x
        y, py = py - q * y, y
        a, b = b, a % b
    return a, px, py


def mod_inv(n, m):
    """:return: mod inv of n, if exists. Otherwise, returns (x, g) where g = gcd(n, m) and x = mod inv of n"""
    g, x, y = x_gcd(n, m)
    if g == 1:
        return x % m
    return x % m, g


def mod_inv_multi(n, m):
    """:return: mod inverses of all numbers till n. (m must be prime)"""
    inv = [1] * (n + 1)
    for i in range(2, m):
        inv[i] = (m - ((m // i) * inv[m % i]) % m) % m
    return inv


def read(typ, times=None, delimiter=None):
    if times is not None:
        return [read(typ, times=None, delimiter=delimiter) for _ in range(times)]
    if isinstance(typ, list):
        return list(map(typ[0], input().strip().split(delimiter)))
    return typ(input().strip())


class BBST:
    pass


class SegmentTree:
    def __init__(self, values, combinator, updater):
        self.original = values
        self.combinator = combinator
        self.updater = updater

        n = len(values)
        tree = [] * (4 * n)

        for i, val in enumerate(values):
            tree[n + i] = val
        for i in reversed(range(n)):
            tree[i] = combinator(tree[2 * i], tree[2 * i + 1])
        self._tree = tree

    def query(self, start, end):
        combinator = self.combinator
        updater = self.updater
        tree = self._tree
        n = len(tree)
        start += n
        end += n

        pass

    def update(self, start, end, value):
        combinator = self.combinator
        updater = self.updater
        tree = self._tree
        n = len(tree)
        pass


class DisjointSet:
    __slots__ = ['_parents', '_sizes']

    def __init__(self) -> None:
        self._parents = {}
        self._sizes = {}

    def find(self, x):
        _parents = self._parents
        x, root = None, x
        while x != root:
            x, root = root, _parents.get(root, root)
        return root

    def size(self, x):
        return self._sizes.get(self.find(x), 1)

    def merge(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y:
            return
        size_x, size_y = self._sizes.get(x, 1), self._sizes.get(y, 1)
        if size_x < size_y:
            x, y = y, x
        self._parents[y] = x
        self._sizes[x] = size_x + size_y
        self._sizes.pop(y, None)


def sieve(n):
    global spf
    spf = [i for i in range(n + 1)]
    spf[0], spf[1] = 2, -1
    i = 2
    while i * i <= n:
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if i < spf[j]:
                    spf[j] = i
        i += 1


def main():
    if Config.prime_sieve is not None:
        sieve(Config.prime_sieve)
    if Config.has_tests:
        for t in range(read(int)):
            solve(t)
    else:
        solve(None)


if __name__ == '__main__':
    spf = []
    main()
