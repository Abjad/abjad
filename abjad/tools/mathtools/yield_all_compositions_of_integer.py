# -*- coding: utf-8 -*-
import itertools


def yield_all_compositions_of_integer(n):
    r'''Yields all compositions of positive integer `n`
    in descending lex order:

    ::

        >>> for integer_composition in mathtools.yield_all_compositions_of_integer(5):
        ...     integer_composition
        ...
        (5,)
        (4, 1)
        (3, 2)
        (3, 1, 1)
        (2, 3)
        (2, 2, 1)
        (2, 1, 2)
        (2, 1, 1, 1)
        (1, 4)
        (1, 3, 1)
        (1, 2, 2)
        (1, 2, 1, 1)
        (1, 1, 3)
        (1, 1, 2, 1)
        (1, 1, 1, 2)
        (1, 1, 1, 1, 1)

    Integer compositions are ordered integer partitions.

    Returns generator of positive integer tuples of length at least ``1``.
    '''
    from abjad.tools import mathtools

    # Finds small values of n easily.
    # Takes ca. 4 seconds for n = 17.

    compositions = []

    x = 0
    string_length = n
    while x < 2 ** (n - 1):
        binary_string = mathtools.integer_to_binary_string(x)
        binary_string = binary_string.zfill(string_length)
        l = [int(c) for c in list(binary_string)]
        partition = []
        g = itertools.groupby(l, lambda x: x)
        for value, group in g:
            partition.append(list(group))
        sublengths = [len(part) for part in partition]
        composition = tuple(sublengths)
        compositions.append(composition)
        x += 1

    for composition in reversed(sorted(compositions)):
        yield composition
