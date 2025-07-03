"""
Enumeration functions.
"""

import functools
import itertools
import typing

from . import math as _math
from . import sequence as _sequence


def _is_restricted_growth_function(sequence) -> bool:
    """
    Is true when ``sequence`` is a restricted growth function. A restricted
    growth function is a sequence ``l`` such that ``l[0] == 1`` and such that
    ``l[i] <= max(l[:i]) + 1`` for ``1 <= i <= len(l)``.

    ..  container:: example

        >>> abjad.enumerate._is_restricted_growth_function([1, 1, 1, 1])
        True

        >>> abjad.enumerate._is_restricted_growth_function([1, 1, 1, 2])
        True

        >>> abjad.enumerate._is_restricted_growth_function([1, 1, 2, 1])
        True

        >>> abjad.enumerate._is_restricted_growth_function([1, 1, 2, 2])
        True

    ..  container:: example

        >>> abjad.enumerate._is_restricted_growth_function([1, 1, 1, 3])
        False

        >>> abjad.enumerate._is_restricted_growth_function([17])
        False

    """
    try:
        for i, n in enumerate(sequence):
            if i == 0:
                if not n == 1:
                    return False
            else:
                if not n <= max(sequence[:i]) + 1:
                    return False
        return True
    except TypeError:
        return False


def _partition_by_rgf(sequence, rgf: list[int]) -> list[list]:
    """
    Partitions ``sequence`` by restricted growth function ``rgf``.

    ..  container:: example

        >>> sequence = list(range(10))
        >>> rgf = [1, 1, 2, 2, 1, 2, 3, 3, 2, 4]

        >>> abjad.enumerate._partition_by_rgf(sequence, rgf)
        [[0, 1, 4], [2, 3, 5, 8], [6, 7], [9]]

    """
    rgf = list(rgf)
    if not _is_restricted_growth_function(rgf):
        raise ValueError(f"must be restricted growth function: {rgf!r}.")
    if not len(sequence) == len(rgf):
        raise ValueError("lengths must be equal.")
    partition = []
    for part_index in range(max(rgf)):
        part: list = []
        partition.append(part)
    for n, part_number in zip(sequence, rgf):
        part_index = part_number - 1
        part = partition[part_index]
        part.append(n)
    partition = [type(sequence)(_) for _ in partition]
    return partition


def _yield_restricted_growth_functions(length) -> typing.Iterator[list[int]]:
    """
    Yields restricted growth functions of ``length`` in lex order.

    ..  container:: example

        >>> rgfs = abjad.enumerate._yield_restricted_growth_functions(4)
        >>> for rgf in rgfs:
        ...     rgf
        ...
        [1, 1, 1, 1]
        [1, 1, 1, 2]
        [1, 1, 2, 1]
        [1, 1, 2, 2]
        [1, 1, 2, 3]
        [1, 2, 1, 1]
        [1, 2, 1, 2]
        [1, 2, 1, 3]
        [1, 2, 2, 1]
        [1, 2, 2, 2]
        [1, 2, 2, 3]
        [1, 2, 3, 1]
        [1, 2, 3, 2]
        [1, 2, 3, 3]
        [1, 2, 3, 4]

    """
    assert _math.is_positive_integer(length), repr(length)
    last_rgf = list(range(1, length + 1))
    rgf = length * [1]
    yield list(rgf)
    while not rgf == last_rgf:
        for i, x in enumerate(reversed(rgf)):
            stop = -(i + 1)
            if x < max(rgf[:stop]) + 1:
                first_part = rgf[:stop]
                increased_part = [rgf[stop] + 1]
                trailing_ones = i * [1]
                rgf = first_part + increased_part + trailing_ones
                yield list(rgf)
                break


def outer_product(argument):
    """
    Yields outer product of sequences in ``argument``. Returns list of lists.

    ..  container:: example

        >>> sequences = [list([1, 2, 3]), list(["a", "b"])]
        >>> for sequence in abjad.enumerate.outer_product(sequences):
        ...     sequence
        ...
        [1, 'a']
        [1, 'b']
        [2, 'a']
        [2, 'b']
        [3, 'a']
        [3, 'b']

    ..  container:: example

        >>> sequences = [[1, 2, 3], ["a", "b"], ["X", "Y"]]
        >>> for sequence in abjad.enumerate.outer_product(sequences):
        ...     sequence
        ...
        [1, 'a', 'X']
        [1, 'a', 'Y']
        [1, 'b', 'X']
        [1, 'b', 'Y']
        [2, 'a', 'X']
        [2, 'a', 'Y']
        [2, 'b', 'X']
        [2, 'b', 'Y']
        [3, 'a', 'X']
        [3, 'a', 'Y']
        [3, 'b', 'X']
        [3, 'b', 'Y']

    ..  container:: example

        >>> sequences = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> for sequence in abjad.enumerate.outer_product(sequences):
        ...     sequence
        ...
        [1, 4, 6]
        [1, 4, 7]
        [1, 4, 8]
        [1, 5, 6]
        [1, 5, 7]
        [1, 5, 8]
        [2, 4, 6]
        [2, 4, 7]
        [2, 4, 8]
        [2, 5, 6]
        [2, 5, 7]
        [2, 5, 8]
        [3, 4, 6]
        [3, 4, 7]
        [3, 4, 8]
        [3, 5, 6]
        [3, 5, 7]
        [3, 5, 8]

    """

    def _helper(sequence_1, sequence_2):
        result = []
        for item_1 in sequence_1:
            for item_2 in sequence_2:
                result.extend([item_1 + [item_2]])
        return result

    argument = list(argument)
    argument[0] = [[_] for _ in argument[0]]
    result = functools.reduce(_helper, argument)
    return result


def yield_combinations(
    argument, minimum_length=None, maximum_length=None
) -> typing.Iterator:
    """
    Yields combinations of sequence items in binary string order.

    ..  container:: example

        >>> sequence = list([1, 2, 3, 4])
        >>> for combination in abjad.enumerate.yield_combinations(sequence):
        ...     combination
        []
        [1]
        [2]
        [1, 2]
        [3]
        [1, 3]
        [2, 3]
        [1, 2, 3]
        [4]
        [1, 4]
        [2, 4]
        [1, 2, 4]
        [3, 4]
        [1, 3, 4]
        [2, 3, 4]
        [1, 2, 3, 4]

    ..  container:: example

        >>> sequence = list([1, 2, 3, 4])
        >>> for combination in abjad.enumerate.yield_combinations(
        ...     sequence,
        ...     minimum_length=3,
        ...     ):
        ...     combination
        [1, 2, 3]
        [1, 2, 4]
        [1, 3, 4]
        [2, 3, 4]
        [1, 2, 3, 4]

    ..  container:: example

        >>> sequence = list([1, 2, 3, 4])
        >>> for combination in abjad.enumerate.yield_combinations(
        ...     sequence,
        ...     maximum_length=2,
        ...     ):
        ...     combination
        []
        [1]
        [2]
        [1, 2]
        [3]
        [1, 3]
        [2, 3]
        [4]
        [1, 4]
        [2, 4]
        [3, 4]

    ..  container:: example

        >>> sequence = list([1, 2, 3, 4])
        >>> for combination in abjad.enumerate.yield_combinations(
        ...     sequence,
        ...     minimum_length=2,
        ...     maximum_length=2,
        ...     ):
        ...     combination
        [1, 2]
        [1, 3]
        [2, 3]
        [1, 4]
        [2, 4]
        [3, 4]

    ..  container:: example

        >>> sequence = list("text")
        >>> for combination in abjad.enumerate.yield_combinations(sequence):
        ...     ''.join([str(_) for _ in combination])
        ''
        't'
        'e'
        'te'
        'x'
        'tx'
        'ex'
        'tex'
        't'
        'tt'
        'et'
        'tet'
        'xt'
        'txt'
        'ext'
        'text'

    """
    length = len(argument)
    for i in range(2**length):
        binary_string = _math.integer_to_binary_string(i)
        binary_string = binary_string.zfill(length)
        sublist = []
        for j, digit in enumerate(reversed(binary_string)):
            if digit == "1":
                sublist.append(argument[j])
        yield_sublist = True
        if minimum_length is not None:
            if len(sublist) < minimum_length:
                yield_sublist = False
        if maximum_length is not None:
            if maximum_length < len(sublist):
                yield_sublist = False
        if yield_sublist:
            if isinstance(argument, str):
                yield "".join(sublist)
            else:
                yield type(argument)(sublist)


def yield_pairs(argument) -> typing.Iterator:
    """
    Yields pairs sequence items.

    ..  container:: example

        Without duplicate items:

        >>> for pair in abjad.enumerate.yield_pairs([1, 2, 3, 4]):
        ...     pair
        ...
        [1, 2]
        [1, 3]
        [1, 4]
        [2, 3]
        [2, 4]
        [3, 4]

    ..  container:: example

        With duplicate items:

        >>> for pair in abjad.enumerate.yield_pairs([1, 1, 1]):
        ...     pair
        ...
        [1, 1]
        [1, 1]
        [1, 1]

    ..  container:: example

        Length-1 sequence:

        >>> for pair in abjad.enumerate.yield_pairs([1]):
        ...     pair
        ...

    ..  container:: example

        Empty sequence:

        >>> for pair in abjad.enumerate.yield_pairs([]):
        ...     pair
        ...

    """
    for i, item in enumerate(argument):
        start = i + 1
        for item_ in argument[start:]:
            pair = [item, item_]
            yield type(argument)(pair)


def yield_partitions(argument) -> typing.Iterator:
    """
    Yields partitions of sequence.

    ..  container:: example

        >>> for partition in abjad.enumerate.yield_partitions([0, 1, 2]):
        ...     partition
        ...
        [[0, 1, 2]]
        [[0, 1], [2]]
        [[0], [1, 2]]
        [[0], [1], [2]]

    ..  container:: example

        >>> for partition in abjad.enumerate.yield_partitions([0, 1, 2, 3]):
        ...     partition
        ...
        [[0, 1, 2, 3]]
        [[0, 1, 2], [3]]
        [[0, 1], [2, 3]]
        [[0, 1], [2], [3]]
        [[0], [1, 2, 3]]
        [[0], [1, 2], [3]]
        [[0], [1], [2, 3]]
        [[0], [1], [2], [3]]

    """
    length = len(argument) - 1
    for i in range(2**length):
        binary_string = _math.integer_to_binary_string(i)
        binary_string = binary_string.zfill(length)
        part = list(argument[0:1])
        partition = [part]
        for n, token in zip(argument[1:], binary_string):
            if int(token) == 0:
                part.append(n)
            else:
                part = [n]
                partition.append(part)
        parts = [type(argument)(_) for _ in partition]
        partition = type(argument)(parts)
        yield partition


def yield_permutations(argument) -> typing.Iterator:
    """
    Yields permutations of sequence.

    ..  container:: example

        >>> for permutation in abjad.enumerate.yield_permutations([1, 2, 3]):
        ...     permutation
        ...
        [1, 2, 3]
        [1, 3, 2]
        [2, 1, 3]
        [2, 3, 1]
        [3, 1, 2]
        [3, 2, 1]

    """
    _argument = list(argument)
    length = len(_argument)
    for permutation in itertools.permutations(tuple(range(length))):
        permutation = type(argument)(permutation)
        yield _sequence.permute(argument, permutation)


def yield_set_partitions(sequence) -> typing.Iterator[list[list]]:
    """
    Yields set partitions of ``sequence`` in order of restricted growth function.

    ..  container:: example

        >>> for set_partition in abjad.enumerate.yield_set_partitions([21, 22, 23, 24]):
        ...     set_partition
        ...
        [[21, 22, 23, 24]]
        [[21, 22, 23], [24]]
        [[21, 22, 24], [23]]
        [[21, 22], [23, 24]]
        [[21, 22], [23], [24]]
        [[21, 23, 24], [22]]
        [[21, 23], [22, 24]]
        [[21, 23], [22], [24]]
        [[21, 24], [22, 23]]
        [[21], [22, 23, 24]]
        [[21], [22, 23], [24]]
        [[21, 24], [22], [23]]
        [[21], [22, 24], [23]]
        [[21], [22], [23, 24]]
        [[21], [22], [23], [24]]

    """
    _sequence = list(sequence)
    length = len(_sequence)
    for rgf in _yield_restricted_growth_functions(length):
        partition = _partition_by_rgf(_sequence, rgf)
        yield partition


def yield_subsequences(
    sequence, minimum_length=0, maximum_length=None
) -> typing.Iterator:
    """
    Yields subsequences of ``sequence``.

    ..  container:: example

        >>> for subsequence in abjad.enumerate.yield_subsequences([0, 1, 2]):
        ...     subsequence
        ...
        []
        [0]
        [0, 1]
        [0, 1, 2]
        [1]
        [1, 2]
        [2]

    ..  container:: example

        >>> for subsequence in abjad.enumerate.yield_subsequences(
        ...     [0, 1, 2, 3, 4],
        ...     minimum_length=3,
        ...     ):
        ...     subsequence
        ...
        [0, 1, 2]
        [0, 1, 2, 3]
        [0, 1, 2, 3, 4]
        [1, 2, 3]
        [1, 2, 3, 4]
        [2, 3, 4]

    ..  container:: example

        >>> for subsequence in abjad.enumerate.yield_subsequences(
        ...     [0, 1, 2, 3, 4],
        ...     maximum_length=3,
        ...     ):
        ...     subsequence
        ...
        []
        [0]
        [0, 1]
        [0, 1, 2]
        [1]
        [1, 2]
        [1, 2, 3]
        [2]
        [2, 3]
        [2, 3, 4]
        [3]
        [3, 4]
        [4]

    ..  container:: example

        >>> for subsequence in abjad.enumerate.yield_subsequences(
        ...     [0, 1, 2, 3, 4],
        ...     minimum_length=3,
        ...     maximum_length=3,
        ...     ):
        ...     subsequence
        ...
        [0, 1, 2]
        [1, 2, 3]
        [2, 3, 4]

    """
    _sequence = sequence
    length = len(_sequence)
    if maximum_length is None:
        maximum_length = length
    for i in range(length):
        start_j = minimum_length + i
        stop_j = min(maximum_length + i, length) + 1
        for j in range(start_j, stop_j):
            if i < j or i == 0:
                subsequence = _sequence[i:j]
                yield subsequence
