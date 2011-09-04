from abjad.tools.mathtools.integer_to_binary_string import integer_to_binary_string
import itertools


def yield_all_compositions_of_integer(n):
    r'''.. versionadded:: 2.0

    Yield all compositions of positive integer `n` in descending lex order::

        abjad> from abjad.tools import mathtools

    ::

        abjad> for integer_composition in mathtools.yield_all_compositions_of_integer(5):
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

    Return generator of positive integer tuples of length at least ``1``.

    .. versionchanged:: 2.0
        renamed ``mathtools.integer_compositions()`` to
        ``mathtools.yield_all_compositions_of_integer()``.
    '''

    from abjad.tools.sequencetools.yield_all_permutations_of_sequence import yield_all_permutations_of_sequence

    # Finds small values of n easily.
    # Takes ca. 4 seconds for n = 17.

    compositions = []

    x = 0
    string_length = n
    while x < 2 ** (n - 1):
        string = integer_to_binary_string(x)
        string = string.zfill(string_length)
        l = [int(c) for c in list(string)]
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
