import builtins
import collections
import copy
import fractions
import itertools
import math
import sys
import typing

from . import cyclictuple as _cyclictuple
from . import enums as _enums
from . import math as _math


def _partition_sequence_cyclically_by_weights_at_least(
    sequence, weights, overhang=False
):
    l_copy = list(sequence)
    result = []
    current_part = []
    target_weight_index = 0
    len_weights = len(weights)
    while l_copy:
        target_weight = weights[target_weight_index % len_weights]
        item = l_copy.pop(0)
        current_part.append(item)
        if target_weight <= _math.weight(current_part):
            result.append(current_part)
            current_part = []
            target_weight_index += 1
    assert not l_copy
    if current_part:
        if overhang:
            result.append(current_part)
    result = [type(sequence)(_) for _ in result]
    return result


def _partition_sequence_cyclically_by_weights_at_most(
    sequence, weights, overhang=False
):
    result = []
    current_part = []
    current_target_weight_index = 0
    current_target_weight = weights[current_target_weight_index]
    l_copy = list(sequence)
    while l_copy:
        current_target_weight = weights[current_target_weight_index % len(weights)]
        item = l_copy.pop(0)
        current_part_weight = _math.weight(current_part)
        candidate_part_weight = current_part_weight + _math.weight([item])
        if candidate_part_weight < current_target_weight:
            current_part.append(item)
        elif candidate_part_weight == current_target_weight:
            current_part.append(item)
            result.append(current_part)
            current_part = []
            current_target_weight_index += 1
        elif current_target_weight < candidate_part_weight:
            if current_part:
                l_copy.insert(0, item)
                result.append(current_part)
                current_part = []
                current_target_weight_index += 1
            else:
                raise Exception("elements in sequence too big.")
        else:
            raise ValueError("candidate and target rates must compare.")
    if current_part:
        if overhang:
            result.append(current_part)
    result = [type(sequence)(_) for _ in result]
    return result


def _partition_sequence_once_by_weights_at_least(sequence, weights, overhang=False):
    result = []
    current_part = []
    l_copy = list(sequence)
    for num_weight, target_weight in enumerate(weights):
        while True:
            try:
                item = l_copy.pop(0)
            except IndexError:
                if num_weight + 1 == len(weights):
                    if current_part:
                        result.append(current_part)
                        break
                raise Exception("too few elements in sequence.")
            current_part.append(item)
            if target_weight <= _math.weight(current_part):
                result.append(current_part)
                current_part = []
                break
    if l_copy:
        if overhang:
            result.append(l_copy)
    result = [type(sequence)(_) for _ in result]
    return result


def _partition_sequence_once_by_weights_at_most(sequence, weights, overhang=False):
    l_copy = list(sequence)
    result = []
    current_part = []
    for target_weight in weights:
        while True:
            try:
                item = l_copy.pop(0)
            except IndexError:
                raise Exception("too few elements in sequence.")
            current_weight = _math.weight(current_part)
            candidate_weight = current_weight + _math.weight([item])
            if candidate_weight < target_weight:
                current_part.append(item)
            elif candidate_weight == target_weight:
                current_part.append(item)
                result.append(current_part)
                current_part = []
                break
            elif target_weight < candidate_weight:
                if current_part:
                    result.append(current_part)
                    current_part = []
                    l_copy.insert(0, item)
                    break
                else:
                    raise Exception("elements in sequence too big.")
            else:
                raise ValueError("candidate and target weights must compare.")
    if overhang:
        left_over = current_part + l_copy
        if left_over:
            result.append(left_over)
    result = [type(sequence)(_) for _ in result]
    return result


def partition_by_counts(
    sequence,
    counts,
    *,
    cyclic: bool = False,
    enchain: bool = False,
    overhang: bool | _enums.Comparison = False,
    reversed_: bool = False,
) -> list:
    r"""
    Partitions ``sequence`` by ``counts``.

    Partitions sequence once by counts without overhang:

    ..  container:: example

        >>> sequence = list(range(16))
        >>> sequence = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=False,
        ...     overhang=False,
        ... )

        >>> sequence
        [[0, 1, 2]]

        >>> for part in sequence:
        ...     part
        [0, 1, 2]

    ..  container:: example

        Partitions sequence once by counts without overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=False,
        ...     overhang=False,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3]
        [4, 5, 6]

    ..  container:: example

        Partitions sequence cyclically by counts without overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=True,
        ...     overhang=False,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9, 10, 11]
        [12, 13, 14]

    ..  container:: example

        Partitions sequence cyclically by counts without overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=True,
        ...     overhang=False,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3]
        [4, 5, 6]
        [7, 8, 9, 10]
        [11, 12, 13]

    ..  container:: example

        Partitions sequence once by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=False,
        ...     overhang=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2]
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    ..  container:: example

        Partitions sequence once by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=False,
        ...     overhang=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3]
        [4, 5, 6]
        [7, 8, 9, 10, 11, 12, 13, 14, 15]

    ..  container:: example

        Partitions sequence cyclically by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=True,
        ...     overhang=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9, 10, 11]
        [12, 13, 14]
        [15]

    ..  container:: example

        Partitions sequence cyclically by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=True,
        ...     overhang=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3]
        [4, 5, 6]
        [7, 8, 9, 10]
        [11, 12, 13]
        [14, 15]

    ..  container:: example

        Reverse-partitions sequence once by counts without overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=False,
        ...     overhang=False,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [13, 14, 15]

    ..  container:: example

        Reverse-partitions sequence once by counts without overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=False,
        ...     overhang=False,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [9, 10, 11]
        [12, 13, 14, 15]

    ..  container:: example

        Reverse-partitions sequence cyclically by counts without overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=True,
        ...     overhang=False,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [1, 2, 3]
        [4, 5, 6]
        [7, 8, 9]
        [10, 11, 12]
        [13, 14, 15]

    ..  container:: example

        Reverse-partitions sequence cyclically by counts without overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=True,
        ...     overhang=False,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [2, 3, 4]
        [5, 6, 7, 8]
        [9, 10, 11]
        [12, 13, 14, 15]

    ..  container:: example

        Reverse-partitions sequence once by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=False,
        ...     overhang=True,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        [13, 14, 15]

    ..  container:: example

        Reverse-partitions sequence once by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=False,
        ...     overhang=True,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3, 4, 5, 6, 7, 8]
        [9, 10, 11]
        [12, 13, 14, 15]

    ..  container:: example

        Reverse-partitions sequence cyclically by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=True,
        ...     overhang=True,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [0]
        [1, 2, 3]
        [4, 5, 6]
        [7, 8, 9]
        [10, 11, 12]
        [13, 14, 15]

    ..  container:: example

        Reverse-partitions sequence cyclically by counts with overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [4, 3],
        ...     cyclic=True,
        ...     overhang=True,
        ...     reversed_=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1]
        [2, 3, 4]
        [5, 6, 7, 8]
        [9, 10, 11]
        [12, 13, 14, 15]

    ..  container:: example

        Partitions sequence once by counts and asserts that sequence partitions
        exactly (with no overhang):

        >>> sequence = list(range(10))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [2, 3, 5],
        ...     cyclic=False,
        ...     overhang=abjad.EXACT,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1]
        [2, 3, 4]
        [5, 6, 7, 8, 9]

    ..  container:: example

        Partitions sequence cyclically by counts and asserts that sequence partitions
        exactly. Exact partitioning means partitioning with no overhang:

        >>> sequence = list(range(10))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [2],
        ...     cyclic=True,
        ...     overhang=abjad.EXACT,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1]
        [2, 3]
        [4, 5]
        [6, 7]
        [8, 9]

    ..  container:: example

        Partitions string:

        >>> sequence = list("some text")
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [3],
        ...     cyclic=False,
        ...     overhang=True,
        ... )

        >>> for part in parts:
        ...     part
        ['s', 'o', 'm']
        ['e', ' ', 't', 'e', 'x', 't']

    ..  container:: example

        Partitions sequence cyclically into enchained parts by counts; truncates
        overhang:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [2, 6],
        ...     cyclic=True,
        ...     enchain=True,
        ...     overhang=False,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1]
        [1, 2, 3, 4, 5, 6]
        [6, 7]
        [7, 8, 9, 10, 11, 12]
        [12, 13]

    ..  container:: example

        Partitions sequence cyclically into enchained parts by counts; returns
        overhang at end:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [2, 6],
        ...     cyclic=True,
        ...     enchain=True,
        ...     overhang=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1]
        [1, 2, 3, 4, 5, 6]
        [6, 7]
        [7, 8, 9, 10, 11, 12]
        [12, 13]
        [13, 14, 15]

    ..  container:: example

        REGRESSION: partitions sequence cyclically into enchained parts by counts;
        does not return false 1-element part at end:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(
        ...     sequence,
        ...     [5],
        ...     cyclic=True,
        ...     enchain=True,
        ...     overhang=True,
        ... )

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3, 4]
        [4, 5, 6, 7, 8]
        [8, 9, 10, 11, 12]
        [12, 13, 14, 15]

    ..  container:: example

        Edge case: empty counts nests sequence and ignores keywords:

        >>> sequence = list(range(16))
        >>> parts = abjad.sequence.partition_by_counts(sequence, [])

        >>> for part in parts:
        ...     part
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    Returns list of ``sequence`` types.
    """
    assert isinstance(cyclic, bool), repr(cyclic)
    assert isinstance(enchain, bool), repr(enchain)
    assert overhang in (True, False, _enums.EXACT), repr(overhang)
    assert isinstance(reversed_, bool), repr(reversed_)
    if not all(isinstance(_, int) and 0 <= _ for _ in counts):
        raise Exception(f"must be nonnegative integers: {counts!r}.")
    if reversed_:
        sequence = type(sequence)(reversed(sequence))
    if counts:
        counts = _cyclictuple.CyclicTuple(counts)
    else:
        return type(sequence)([sequence])
    result = []
    i, start = 0, 0
    while True:
        count = counts[i]
        stop = start + count
        part = sequence[start:stop]
        if len(sequence) < stop:
            if enchain and len(part) == 1:
                part = None
            break
        result.append(part)
        start = stop
        i += 1
        if not cyclic and len(counts) <= i:
            part = sequence[start:]
            break
        if enchain:
            start -= 1
    if part:
        if overhang is True:
            result.append(part)
        elif overhang is _enums.EXACT and len(part) == count:
            result.append(part)
        elif overhang is _enums.EXACT and len(part) != count:
            raise Exception("sequence does not partition exactly.")
    if reversed_:
        result_ = []
        for part in reversed(result):
            part_type = type(part)
            part = reversed(part)
            part = part_type(part)
            result_.append(part)
        result = result_
    return result


def partition_by_ratio_of_lengths(sequence, ratio: tuple[int, ...]) -> list:
    r"""
    Partitions ``sequence`` by ``ratio`` of lengths.

    Partitions sequence by ``1:1:1`` ratio:

    ..  container:: example

        >>> numbers = list(range(10))
        >>> ratio = (1, 1, 1)

        >>> for part in abjad.sequence.partition_by_ratio_of_lengths(numbers, ratio):
        ...     part
        [0, 1, 2]
        [3, 4, 5, 6]
        [7, 8, 9]

    ..  container:: example

        Partitions sequence by ``1:1:2`` ratio:

        >>> numbers = list(range(10))
        >>> ratio = (1, 1, 2)

        >>> for part in abjad.sequence.partition_by_ratio_of_lengths(numbers, ratio):
        ...     part
        [0, 1, 2]
        [3, 4]
        [5, 6, 7, 8, 9]

    Returns list of ``sequence`` types.
    """
    assert isinstance(ratio, tuple), repr(ratio)
    length = len(sequence)
    counts = _math.partition_integer_by_ratio(length, ratio)
    parts = partition_by_counts(sequence, counts, cyclic=False, overhang=_enums.EXACT)
    return parts


def partition_by_ratio_of_weights(sequence, weights: typing.Sequence[int]) -> list:
    """
    Partitions ``sequence`` by ratio of ``weights``.

    ..  container:: example

        >>> ratio = (1, 1, 1)
        >>> sequence = list(10 * [1])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [1, 1, 1]
        [1, 1, 1, 1]
        [1, 1, 1]

    ..  container:: example

        >>> ratio = (1, 1, 1, 1)
        >>> sequence = list(10 * [1])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [1, 1, 1]
        [1, 1]
        [1, 1, 1]
        [1, 1]

    ..  container:: example

        >>> ratio = (2, 2, 3)
        >>> sequence = list(10 * [1])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [1, 1, 1]
        [1, 1, 1]
        [1, 1, 1, 1]

    ..  container:: example

        >>> ratio = (3, 2, 2)
        >>> sequence = list(10 * [1])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [1, 1, 1, 1]
        [1, 1, 1]
        [1, 1, 1]

    ..  container:: example

        >>> ratio = (1, 1)
        >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
        >>> sequence = list(items)
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [1, 1, 1, 1, 1, 1, 2, 2]
        [2, 2, 2, 2]

    ..  container:: example

        >>> ratio = (1, 1, 1)
        >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
        >>> sequence = list(items)
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [1, 1, 1, 1, 1, 1]
        [2, 2, 2]
        [2, 2, 2]

    ..  container:: example

        >>> ratio = (1, 1, 1)
        >>> sequence = list([5, 5])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [5]
        [5]
        []

    ..  container:: example

        >>> ratio = (1, 1, 1, 1)
        >>> sequence = list([5, 5])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [5]
        []
        [5]
        []

    ..  container:: example

        >>> ratio = (2, 2, 3)
        >>> sequence = list([5, 5])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [5]
        [5]
        []

    ..  container:: example

        >>> ratio = (3, 2, 2)
        >>> sequence = list([5, 5])
        >>> sequence = abjad.sequence.partition_by_ratio_of_weights(sequence, ratio)
        >>> for item in sequence:
        ...     item
        ...
        [5]
        [5]
        []

    Rounded weight-proportions of sequences returned equal to rounded ``weights``.

    Returns list of ``sequence`` types.
    """
    assert all(isinstance(_, int | float | fractions.Fraction) for _ in sequence)
    sequence_weight = _math.weight(sequence)
    partitioned_weights = _math.partition_integer_by_ratio(sequence_weight, weights)
    cumulative_weights = _math.cumulative_sums(partitioned_weights, start=None)
    items = []
    sublist: list[typing.Any] = []
    items.append(sublist)
    current_cumulative_weight = cumulative_weights.pop(0)
    for item in sequence:
        sublist.append(item)
        while current_cumulative_weight <= _math.weight(flatten(items, depth=-1)):
            try:
                current_cumulative_weight = cumulative_weights.pop(0)
                sublist = []
                items.append(sublist)
            except IndexError:
                break
    result = [type(sequence)(_) for _ in items]
    return result


def partition_by_weights(
    sequence,
    weights: typing.Sequence[int | fractions.Fraction],
    *,
    cyclic: bool = False,
    overhang: bool = False,
    allow_part_weights: _enums.Comparison = _enums.EXACT,
) -> list:
    r"""
    Partitions ``sequence`` by ``weights`` exactly.

    >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]

    ..  container:: example

        Partitions sequence once by weights with overhang:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [3, 9],
        ...     cyclic=False,
        ...     overhang=False,
        ... ):
        ...     item
        ...
        [3]
        [3, 3, 3]

    ..  container:: example

        Partitions sequence once by weights. Allows overhang:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [3, 9],
        ...     cyclic=False,
        ...     overhang=True,
        ... ):
        ...     item
        ...
        [3]
        [3, 3, 3]
        [4, 4, 4, 4, 5]

    ..  container:: example

        Partitions sequence cyclically by weights:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [12],
        ...     cyclic=True,
        ...     overhang=False,
        ... ):
        ...     item
        ...
        [3, 3, 3, 3]
        [4, 4, 4]

    ..  container:: example

        Partitions sequence cyclically by weights. Allows overhang:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [12],
        ...     cyclic=True,
        ...     overhang=True,
        ... ):
        ...     item
        ...
        [3, 3, 3, 3]
        [4, 4, 4]
        [4, 5]

    >>> sequence = list([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

    ..  container:: example

        Partitions sequence once by weights. Allows part weights to be just less than
        specified:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 4],
        ...     cyclic=False,
        ...     overhang=False,
        ...     allow_part_weights=abjad.LESS,
        ... ):
        ...     item
        ...
        [3, 3, 3]
        [3]

    ..  container:: example

        Partitions sequence once by weights. Allows part weights to be just less than
        specified. Allows overhang:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 4],
        ...     cyclic=False,
        ...     overhang=True,
        ...     allow_part_weights=abjad.LESS,
        ... ):
        ...     item
        ...
        [3, 3, 3]
        [3]
        [4, 4, 4, 4, 5, 5]

    ..  container:: example

        Partitions sequence cyclically by weights. Allows part weights to be just
        less than specified:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 5],
        ...     cyclic=True,
        ...     overhang=False,
        ...     allow_part_weights=abjad.LESS,
        ... ):
        ...     item
        ...
        [3, 3, 3]
        [3]
        [4, 4]
        [4]
        [4, 5]
        [5]

    ..  container:: example

        Partitions sequence cyclically by weights. Allows part weights to be just
        less than specified. Allows overhang:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 5],
        ...     cyclic=True,
        ...     overhang=True,
        ...     allow_part_weights=abjad.LESS,
        ... ):
        ...     item
        ...
        [3, 3, 3]
        [3]
        [4, 4]
        [4]
        [4, 5]
        [5]

    >>> sequence = list([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

    ..  container:: example

        Partitions sequence once by weights. Allow part weights to be just more than
        specified:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 4],
        ...     cyclic=False,
        ...     overhang=False,
        ...     allow_part_weights=abjad.MORE,
        ... ):
        ...     item
        ...
        [3, 3, 3, 3]
        [4]

    ..  container:: example

        Partitions sequence once by weights. Allows part weights to be just more than
        specified. Allows overhang:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 4],
        ...     cyclic=False,
        ...     overhang=True,
        ...     allow_part_weights=abjad.MORE,
        ... ):
        ...     item
        ...
        [3, 3, 3, 3]
        [4]
        [4, 4, 4, 5, 5]

    ..  container:: example

        Partitions sequence cyclically by weights. Allows part weights to be just
        more than specified:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 4],
        ...     cyclic=True,
        ...     overhang=False,
        ...     allow_part_weights=abjad.MORE,
        ... ):
        ...     item
        ...
        [3, 3, 3, 3]
        [4]
        [4, 4, 4]
        [5]

    ..  container:: example

        Partitions sequence cyclically by weights. Allows part weights to be just
        more than specified. Allows overhang:

        >>> for item in abjad.sequence.partition_by_weights(
        ...     sequence,
        ...     [10, 4],
        ...     cyclic=True,
        ...     overhang=True,
        ...     allow_part_weights=abjad.MORE,
        ... ):
        ...     item
        ...
        [3, 3, 3, 3]
        [4]
        [4, 4, 4]
        [5]
        [5]

    Returns list of ``sequence`` types.
    """
    if allow_part_weights is _enums.EXACT:
        candidate = type(sequence)(sequence)
        candidate = split(candidate, weights, cyclic=cyclic, overhang=overhang)
        flattened_candidate = flatten(candidate, depth=-1)
        if flattened_candidate == sequence[: len(flattened_candidate)]:
            return candidate
        else:
            raise Exception("can not partition exactly.")
    elif allow_part_weights is _enums.MORE:
        if not cyclic:
            result = _partition_sequence_once_by_weights_at_least(
                sequence, weights, overhang=overhang
            )
        else:
            result = _partition_sequence_cyclically_by_weights_at_least(
                sequence, weights, overhang=overhang
            )
    elif allow_part_weights is _enums.LESS:
        if not cyclic:
            result = _partition_sequence_once_by_weights_at_most(
                sequence, weights, overhang=overhang
            )
        else:
            result = _partition_sequence_cyclically_by_weights_at_most(
                sequence, weights, overhang=overhang
            )
    else:
        message = "allow_part_weights must be ordinal constant: {!r}."
        message = message.format(allow_part_weights)
        raise ValueError(message)
    return result


def split(
    sequence,
    weights: typing.Sequence[int | fractions.Fraction],
    *,
    cyclic: bool = False,
    overhang: bool = False,
) -> list:
    r"""
    Splits ``sequence`` by ``weights``.

    ..  container:: example

        Splits sequence cyclically by weights with overhang:

        >>> sequence = list([10, -10, 10, -10])

        >>> for part in abjad.sequence.split(
        ...     sequence,
        ...     (3, 15, 3),
        ...     cyclic=True,
        ...     overhang=True,
        ... ):
        ...     part
        ...
        [3]
        [7, -8]
        [-2, 1]
        [3]
        [6, -9]
        [-1]

    ..  container:: example

        Splits sequence once by weights with overhang:

        >>> for part in abjad.sequence.split(
        ...     sequence,
        ...     (3, 15, 3),
        ...     cyclic=False,
        ...     overhang=True,
        ... ):
        ...     part
        ...
        [3]
        [7, -8]
        [-2, 1]
        [9, -10]

    ..  container:: example

        Splits sequence once by weights without overhang:

        >>> for part in abjad.sequence.split(
        ...     sequence,
        ...     (3, 15, 3),
        ...     cyclic=False,
        ...     overhang=False,
        ... ):
        ...     part
        ...
        [3]
        [7, -8]
        [-2, 1]

    ..  container:: example

        REGRESSION. Splits sequence of durations cyclically by weights
        with overhang; then expresses durations as pairs with denominator:

        >>> sequence = list([
        ...     abjad.Duration(20, 2),
        ...     abjad.Duration(-20, 2),
        ...     abjad.Duration(20, 2),
        ...     abjad.Duration(-20, 2),
        ... ])

        >>> for part in abjad.sequence.split(
        ...     sequence,
        ...     (3, 15, 3),
        ...     cyclic=True,
        ...     overhang=True,
        ... ):
        ...     [abjad.duration.with_denominator(_, 2) for _ in part]
        ...
        [(6, 2)]
        [(14, 2), (-16, 2)]
        [(-4, 2), (2, 2)]
        [(6, 2)]
        [(12, 2), (-18, 2)]
        [(-2, 2)]

    Returns list of ``sequence`` types.
    """
    result = []
    current_index = 0
    current_piece: list[typing.Any] = []
    if cyclic:
        weights = repeat_to_weight(
            weights, _math.weight(sequence), allow_total=_enums.LESS
        )
    for weight in weights:
        current_piece_weight = _math.weight(current_piece)
        while current_piece_weight < weight:
            current_piece.append(sequence[current_index])
            current_index += 1
            current_piece_weight = _math.weight(current_piece)
        if current_piece_weight == weight:
            current_piece_ = type(sequence)(current_piece)
            result.append(current_piece_)
            current_piece = []
        elif weight < current_piece_weight:
            overage = current_piece_weight - weight
            current_last_element = current_piece.pop(-1)
            needed = abs(current_last_element) - overage
            needed *= _math.sign(current_last_element)
            current_piece.append(needed)
            current_piece_ = type(sequence)(current_piece)
            result.append(current_piece_)
            overage *= _math.sign(current_last_element)
            current_piece = [overage]
    if overhang:
        last_piece = current_piece
        last_piece.extend(sequence[current_index:])
        if last_piece:
            last_piece_ = type(sequence)(last_piece)
            result.append(last_piece_)
    return result


def filter(sequence, predicate: typing.Callable | None = None):
    """
    Filters ``sequence`` by callable ``predicate``.

    ..  container:: example

        By length:

        >>> sequence = [[1], [2, 3, [4]], [5], [6, 7, [8]]]

        >>> abjad.sequence.filter(sequence, lambda _: len(_) == 1)
        [[1], [5]]

        By duration:

        >>> staff = abjad.Staff("c'4. d'8 e'4. f'8 g'2")
        >>> sequence = list(staff)

        >>> abjad.sequence.filter(
        ...     sequence, lambda _: _.written_duration == abjad.Duration(1, 8)
        ... )
        [Note("d'8"), Note("f'8")]

    Returns ``sequence`` type.
    """
    if predicate is None:
        return sequence[:]
    items = []
    for item in sequence:
        if predicate(item):
            items.append(item)
    return type(sequence)(items)


# creates an iterator that can generate a flattened list,
# descending down into child elements to a depth given in the arguments.
# note that depth < 0 is effectively equivalent to infinity.
def _flatten_helper(sequence, classes, depth):
    if not isinstance(sequence, classes):
        yield sequence
    elif depth == 0:
        for item in sequence:
            yield item
    else:
        for item in sequence:
            # flatten an iterable by one level
            depth_ = depth - 1
            for item_ in _flatten_helper(item, classes, depth_):
                yield item_


def flatten(
    sequence, *, classes: typing.Sequence[typing.Type] | None = None, depth: int = 1
):
    r"""
    Flattens ``sequence``.

    ..  container:: example

        Flattens sequence:

        >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
        >>> abjad.sequence.flatten(sequence)
        [1, 2, 3, [4], 5, 6, 7, [8]]

        Flattens sequence to depth 2:

        >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
        >>> abjad.sequence.flatten(sequence, depth=2)
        [1, 2, 3, 4, 5, 6, 7, 8]

        Flattens sequence to depth -1:

        >>> sequence = [1, [2, 3, [4]], 5, [6, 7, [8]]]
        >>> abjad.sequence.flatten(sequence, depth=-1)
        [1, 2, 3, 4, 5, 6, 7, 8]

        Flattens tuples in sequence only:

        >>> sequence = ["ab", "cd", ("ef", "gh"), ("ij", "kl")]
        >>> abjad.sequence.flatten(sequence, classes=(tuple, list))
        ['ab', 'cd', 'ef', 'gh', 'ij', 'kl']

    Returns ``sequence`` type.
    """
    if classes is None:
        classes = (collections.abc.Sequence,)
    items = _flatten_helper(sequence, classes, depth)
    return type(sequence)(items)


def group_by(sequence, predicate: typing.Callable | None = None) -> list:
    """
    Groups ``sequence`` items by value of items.

    ..  container:: example

        >>> items = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]
        >>> sequence = list(items)
        >>> for item in abjad.sequence.group_by(sequence):
        ...     item
        ...
        [0, 0]
        [-1, -1]
        [2]
        [3]
        [-5]
        [1, 1]
        [5]
        [-5]

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d' d' e' e' e'")
        >>> predicate = lambda _: abjad.PitchSet([_])
        >>> sequence = list(staff)
        >>> for item in abjad.sequence.group_by(sequence, predicate):
        ...     item
        ...
        [Note("c'8")]
        [Note("d'8"), Note("d'8")]
        [Note("e'8"), Note("e'8"), Note("e'8")]

    Returns list of ``sequence`` types.
    """
    items = []
    if predicate is None:
        pairs = itertools.groupby(sequence, lambda _: _)
        for count, group in pairs:
            item = type(sequence)(group)
            items.append(item)
    else:
        pairs = itertools.groupby(sequence, predicate)
        for count, group in pairs:
            item = type(sequence)(group)
            items.append(item)
    return items


def has_duplicates(sequence):
    """
    Is true when ``sequence`` has duplicates.

    ..  container::

        >>> abjad.sequence.has_duplicates([0, 1, 2, 3, 4])
        False

        >>> abjad.sequence.has_duplicates([0, 1, 2, 3, 3])
        True

        >>> abjad.sequence.has_duplicates([0, 1, 0, 1, 0])
        True

    """
    return len(set(sequence)) < len(sequence)


def is_decreasing(sequence, *, strict: bool = True) -> bool:
    """
    Is true when ``sequence`` is decreasing.

    Is true when sequence is strictly decreasing:

    ..  container:: example

        >>> abjad.sequence.is_decreasing([5, 4, 3, 2, 1, 0], strict=True)
        True

        >>> abjad.sequence.is_decreasing([3, 3, 3, 2, 1, 0], strict=True)
        False

        >>> abjad.sequence.is_decreasing([3, 3, 3, 3, 3, 3], strict=True)
        False

        >>> abjad.sequence.is_decreasing([], strict=True)
        True

    ..  container:: example

        Is true when sequence decreases monotonically:

        >>> abjad.sequence.is_decreasing([5, 4, 3, 2, 1, 0], strict=False)
        True

        >>> abjad.sequence.is_decreasing([3, 3, 3, 2, 1, 0], strict=False)
        True

        >>> abjad.sequence.is_decreasing([3, 3, 3, 3, 3, 3], strict=False)
        True

        >>> abjad.sequence.is_decreasing([], strict=False)
        True

    """
    if strict:
        try:
            previous = None
            for current in sequence:
                if previous is not None:
                    if not current < previous:
                        return False
                previous = current
            return True
        except TypeError:
            return False
    else:
        try:
            previous = None
            for current in sequence:
                if previous is not None:
                    if not current <= previous:
                        return False
                previous = current
            return True
        except TypeError:
            return False


def is_increasing(sequence, *, strict: bool = True) -> bool:
    """
    Is true when ``sequence`` is increasing.

    Is true when sequence is strictly increasing:

    ..  container:: example

        >>> abjad.sequence.is_increasing([0, 1, 2, 3, 4, 5], strict=True)
        True

        >>> abjad.sequence.is_increasing([0, 1, 2, 3, 3, 3], strict=True)
        False

        >>> abjad.sequence.is_increasing([3, 3, 3, 3, 3, 3], strict=True)
        False

        >>> abjad.sequence.is_increasing([], strict=True)
        True

    ..  container:: example

        Is true when sequence increases monotonically:

        >>> abjad.sequence.is_increasing([0, 1, 2, 3, 4, 5], strict=False)
        True

        >>> abjad.sequence.is_increasing([0, 1, 2, 3, 3, 3], strict=False)
        True

        >>> abjad.sequence.is_increasing([3, 3, 3, 3, 3, 3], strict=False)
        True

        >>> abjad.sequence.is_increasing([], strict=False)
        True

    """
    if strict:
        try:
            previous = None
            for current in sequence:
                if previous is not None:
                    if not previous < current:
                        return False
                previous = current
            return True
        except TypeError:
            return False
    else:
        try:
            previous = None
            for current in sequence:
                if previous is not None:
                    if not previous <= current:
                        return False
                previous = current
            return True
        except TypeError:
            return False


def is_permutation(sequence) -> bool:
    """
    Is true when ``sequence`` is a permutation.

    ..  container:: example

        >>> abjad.sequence.is_permutation([4, 5, 0, 3, 2, 1])
        True

        >>> abjad.sequence.is_permutation([1, 1, 5, 3, 2, 1])
        False

    """
    return tuple(sorted(sequence)) == tuple(range(len(sequence)))


def is_repetition_free(sequence) -> bool:
    """
    Is true when ``sequence`` is repetition-free.

    ..  container:: example

        >>> abjad.sequence.is_repetition_free([0, 1, 2, 6, 7, 8])
        True

        >>> abjad.sequence.is_repetition_free([])
        True

        >>> abjad.sequence.is_repetition_free([0, 1, 2, 2, 7, 8])
        False

    """
    try:
        for left, right in nwise(sequence):
            if left == right:
                return False
        return True
    except TypeError:
        return False


def join(sequence):
    """
    Join subsequences in ``sequence``.

    ..  container:: example

        >>> items = [(1, 2, 3), (), (4, 5), (), (6,)]
        >>> sequence = list(items)
        >>> sequence
        [(1, 2, 3), (), (4, 5), (), (6,)]

        >>> abjad.sequence.join(sequence)
        [(1, 2, 3, 4, 5, 6)]

    Returns ``sequence`` type.
    """
    if not sequence:
        return type(sequence)()
    item = sequence[0]
    for item_ in sequence[1:]:
        item += item_
    return type(sequence)([item])


def nwise(
    sequence, n: int = 2, *, cyclic: bool = False, wrapped: bool = False
) -> typing.Iterator:
    """
    Iterates ``sequence`` ``n`` items at a time.

    Iterates items 2 at a time:

    ..  container:: example

        >>> sequence = list(range(10))
        >>> for item in abjad.sequence.nwise(sequence):
        ...     item
        ...
        [0, 1]
        [1, 2]
        [2, 3]
        [3, 4]
        [4, 5]
        [5, 6]
        [6, 7]
        [7, 8]
        [8, 9]

        Iterates items 3 at a time:

        >>> sequence = list(range(10))
        >>> for item in abjad.sequence.nwise(sequence, n=3):
        ...     item
        ...
        [0, 1, 2]
        [1, 2, 3]
        [2, 3, 4]
        [3, 4, 5]
        [4, 5, 6]
        [5, 6, 7]
        [6, 7, 8]
        [7, 8, 9]

        Iterates items 2 at a time. Wraps around at end:

        >>> sequence = list(range(10))
        >>> for item in abjad.sequence.nwise(sequence, n=2, wrapped=True):
        ...     item
        ...
        [0, 1]
        [1, 2]
        [2, 3]
        [3, 4]
        [4, 5]
        [5, 6]
        [6, 7]
        [7, 8]
        [8, 9]
        [9, 0]

        Iterates items 3 at a time. Wraps around at end:

        >>> sequence = list(range(10))
        >>> for item in abjad.sequence.nwise(sequence, n=3, wrapped=True):
        ...     item
        ...
        [0, 1, 2]
        [1, 2, 3]
        [2, 3, 4]
        [3, 4, 5]
        [4, 5, 6]
        [5, 6, 7]
        [6, 7, 8]
        [7, 8, 9]
        [8, 9, 0]
        [9, 0, 1]

        Iterates items 2 at a time. Cycles indefinitely:

        >>> sequence = list(range(10))
        >>> pairs = abjad.sequence.nwise(sequence, n=2, cyclic=True)
        >>> for _ in range(15):
        ...     next(pairs)
        ...
        [0, 1]
        [1, 2]
        [2, 3]
        [3, 4]
        [4, 5]
        [5, 6]
        [6, 7]
        [7, 8]
        [8, 9]
        [9, 0]
        [0, 1]
        [1, 2]
        [2, 3]
        [3, 4]
        [4, 5]

        Returns infinite generator.

        Iterates items 3 at a time. Cycles indefinitely:

        >>> sequence = list(range(10))
        >>> triples = abjad.sequence.nwise(sequence, n=3, cyclic=True)
        >>> for _ in range(15):
        ...     next(triples)
        ...
        [0, 1, 2]
        [1, 2, 3]
        [2, 3, 4]
        [3, 4, 5]
        [4, 5, 6]
        [5, 6, 7]
        [6, 7, 8]
        [7, 8, 9]
        [8, 9, 0]
        [9, 0, 1]
        [0, 1, 2]
        [1, 2, 3]
        [2, 3, 4]
        [3, 4, 5]
        [4, 5, 6]

        Returns infinite generator.

        Iterates items 1 at a time:

        >>> sequence = list(range(10))
        >>> for item in abjad.sequence.nwise(sequence, n=1):
        ...     item
        ...
        [0]
        [1]
        [2]
        [3]
        [4]
        [5]
        [6]
        [7]
        [8]
        [9]

    Ignores ``wrapped`` when ``cyclic=True``.
    """
    if cyclic:
        item_buffer = []
        long_enough = False
        for item in sequence:
            item_buffer.append(item)
            if not long_enough:
                if n <= len(item_buffer):
                    long_enough = True
            if long_enough:
                yield type(sequence)(item_buffer[-n:])
        len_sequence = len(item_buffer)
        current = len_sequence - n + 1
        while True:
            output = []
            for local_offset in range(n):
                index = (current + local_offset) % len_sequence
                output.append(item_buffer[index])
            yield type(sequence)(output)
            current += 1
            current %= len_sequence
    elif wrapped:
        first_n_minus_1: list[typing.Any] = []
        item_buffer = []
        for item in sequence:
            item_buffer.append(item)
            if len(item_buffer) == n:
                yield type(sequence)(item_buffer)
                item_buffer.pop(0)
            if len(first_n_minus_1) < n - 1:
                first_n_minus_1.append(item)
        item_buffer = item_buffer + first_n_minus_1
        if item_buffer:
            for x in range(n - 1):
                stop = x + n
                yield type(sequence)(item_buffer[x:stop])
    else:
        item_buffer = []
        for item in sequence:
            item_buffer.append(item)
            if len(item_buffer) == n:
                yield type(sequence)(item_buffer)
                item_buffer.pop(0)


def permute(sequence, permutation: typing.Sequence[int]):
    r"""
    Permutes ``sequence`` by ``permutation``.

    ..  container:: example

        >>> abjad.sequence.permute([10, 11, 12, 13, 14, 15], [5, 4, 0, 1, 2, 3])
        [15, 14, 10, 11, 12, 13]

        >>> abjad.sequence.permute([11, 12, 13, 14], [1, 0, 3, 2])
        [12, 11, 14, 13]

    ..  container:: exception

        Raises exception when lengths do not match:

        >>> abjad.sequence.permute([1, 2, 3, 4, 5, 6], [3, 0, 1, 2])
        Traceback (most recent call last):
            ...
        ValueError: permutation [3, 0, 1, 2] must match length of [1, 2, 3, 4, 5, 6].

    Returns ``sequence`` type.
    """
    permutation = type(sequence)(permutation)
    if not is_permutation(permutation):
        raise ValueError(f"must be permutation: {permutation!r}.")
    if len(permutation) != len(sequence):
        message = f"permutation {permutation!r} must match length of {sequence !r}."
        raise ValueError(message)
    result = []
    for i, item in enumerate(sequence):
        j = permutation[i]
        item_ = sequence[j]
        result.append(item_)
    return type(sequence)(result)


def remove(sequence, pattern):
    """
    Removes ``sequence`` items at indices specified by ``pattern``.

    ..  container:: example

        >>> sequence = list(range(15))

        >>> abjad.sequence.remove(sequence, abjad.index([2, 3]))
        [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        Removes elements and indices -2 and -3:

        >>> abjad.sequence.remove(sequence, abjad.index([-2, -3]))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14]

        >>> abjad.sequence.remove(sequence, abjad.index([2, 3], 4))
        [0, 1, 4, 5, 8, 9, 12, 13]

        >>> abjad.sequence.remove(sequence, abjad.index([-2, -3], 4))
        [2, 3, 6, 7, 10, 11, 14]

        >>> abjad.sequence.remove(sequence, abjad.index([]))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        >>> abjad.sequence.remove(sequence, abjad.index([97, 98, 99]))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        Removes no elements:

        >>> abjad.sequence.remove(sequence, abjad.index([-97, -98, -99]))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    Returns ``sequence`` type.
    """
    items = []
    length = len(sequence)
    indices = pattern.indices
    period = pattern.period or length
    if indices is None:
        indices = range(length)
    new_indices = []
    for i in indices:
        if length < abs(i):
            continue
        if i < 0:
            i = length + i
        i = i % period
        new_indices.append(i)
    indices = new_indices
    indices.sort()
    for i, item in enumerate(sequence):
        if i % period not in indices:
            items.append(item)
    return type(sequence)(items)


def remove_repeats(sequence):
    """
    Removes repeats from ``sequence``.

    ..  container:: example

        >>> abjad.sequence.remove_repeats([31, 31, 35, 35, 31, 31, 31, 31, 35])
        [31, 35, 31, 35]

    Returns ``sequence`` type.
    """
    items = [sequence[0]]
    for item in sequence[1:]:
        if item != items[-1]:
            items.append(item)
    return type(sequence)(items)


def repeat(sequence, n: int = 1) -> list:
    r"""
    Repeats ``sequence``, to a total of ``n`` copies.

    ..  container:: example

        >>> abjad.sequence.repeat([1, 2, 3], n=0)
        []

        >>> abjad.sequence.repeat([1, 2, 3], n=1)
        [[1, 2, 3]]

        >>> abjad.sequence.repeat([1, 2, 3], n=2)
        [[1, 2, 3], [1, 2, 3]]

    Returns list of ``sequence`` types.
    """
    sequences = []
    for i in range(n):
        sequences.append(sequence[:])
    return sequences


def repeat_to_length(sequence, length: int = 0, *, start: int = 0):
    """
    Repeats ``sequence`` to ``length``.

    ..  container:: example

        Repeats list to length 11:

        >>> abjad.sequence.repeat_to_length([0, 1, 2, 3, 4], 11)
        [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

        >>> abjad.sequence.repeat_to_length([0, 1, 2, 3, 4], 11, start=2)
        [2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2]

        >>> abjad.sequence.repeat_to_length([0, -1, -2, -3, -4], 11)
        [0, -1, -2, -3, -4, 0, -1, -2, -3, -4, 0]

        >>> abjad.sequence.repeat_to_length([0, -1, -2, -3, -4], 0)
        []

        >>> abjad.sequence.repeat_to_length([1, 2, 3], 10, start=100)
        [2, 3, 1, 2, 3, 1, 2, 3, 1, 2]

    Returns ``sequence`` type.
    """
    assert _math.is_nonnegative_integer(length), repr(length)
    assert len(sequence), repr(sequence)
    items = []
    start %= len(sequence)
    stop_index = start + length
    repetitions = int(math.ceil(float(stop_index) / len(sequence)))
    for i in range(repetitions):
        for item in sequence:
            items.append(item)
    return type(sequence)(items[start:stop_index])


def repeat_to_weight(
    sequence,
    weight: int | fractions.Fraction,
    *,
    allow_total: _enums.Comparison = _enums.EXACT,
):
    """
    Repeats ``sequence`` to ``weight``.

    ..  container:: example

        Repeats sequence to weight of 23 exactly:

        >>> abjad.sequence.repeat_to_weight([5, -5, -5], 23)
        [5, -5, -5, 5, -3]

        Repeats sequence to weight of 23 more:

        >>> abjad.sequence.repeat_to_weight([5, -5, -5], 23, allow_total=abjad.MORE)
        [5, -5, -5, 5, -5]

        Repeats sequence to weight of 23 or less:

        >>> abjad.sequence.repeat_to_weight([5, -5, -5], 23, allow_total=abjad.LESS)
        [5, -5, -5, 5]

        >>> sequence = [abjad.Duration(3, 16)]
        >>> weight = abjad.Duration(5, 4)
        >>> sequence = abjad.sequence.repeat_to_weight(sequence, weight)
        >>> sum(sequence)
        Duration(5, 4)

        >>> [abjad.duration.with_denominator(_, 16) for _ in sequence]
        [(3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]

    Returns ``sequence`` type.
    """
    assert 0 <= weight
    if allow_total is _enums.EXACT:
        sequence_weight = _math.weight(sequence)
        complete_repetitions = int(math.ceil(float(weight) / float(sequence_weight)))
        items = list(sequence)
        items = complete_repetitions * items
        overage = complete_repetitions * sequence_weight - weight
        for item in reversed(items):
            if 0 < overage:
                element_weight = abs(item)
                candidate_overage = overage - element_weight
                if 0 <= candidate_overage:
                    overage = candidate_overage
                    items.pop()
                else:
                    absolute_amount_to_keep = element_weight - overage
                    assert 0 < absolute_amount_to_keep
                    signed_amount_to_keep = absolute_amount_to_keep
                    signed_amount_to_keep *= _math.sign(item)
                    items.pop()
                    items.append(signed_amount_to_keep)
                    break
            else:
                break
    elif allow_total is _enums.LESS:
        items = [sequence[0]]
        i = 1
        while _math.weight(items) < weight:
            items.append(sequence[i % len(sequence)])
            i += 1
        if weight < _math.weight(items):
            items = items[:-1]
        return type(sequence)(items)
    elif allow_total is _enums.MORE:
        items = [sequence[0]]
        i = 1
        while _math.weight(items) < weight:
            items.append(sequence[i % len(sequence)])
            i += 1
        return type(sequence)(items)
    else:
        raise ValueError(f"is not an ordinal value constant: {allow_total!r}.")
    return type(sequence)(items)


def replace(sequence, old, new):
    """
    Replaces every ``old``-valued item in ``sequence`` with ``new``.

    ..  container:: example

        >>> sequence = [0, 2, 3, 0, 2, 3, 0, 2, 3]
        >>> abjad.sequence.replace(sequence, 0, 1)
        [1, 2, 3, 1, 2, 3, 1, 2, 3]

    Returns ``sequence`` type.
    """
    items = []
    for item in sequence:
        if item == old:
            new_copy = copy.copy(new)
            items.append(new_copy)
        else:
            items.append(item)
    return type(sequence)(items)


def replace_at(sequence, indices, new_material):
    """
    Replaces items at ``indices`` with ``new_material``.

    ..  container:: example

        Replaces items at indices 0, 2, 4, 6:

        >>> sequence = list(range(16))
        >>> abjad.sequence.replace_at(
        ...     sequence,
        ...     ([0], 2),
        ...     (['A', 'B', 'C', 'D'], None),
        ... )
        ['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15]

        Replaces elements at indices 0, 1, 8, 13:

        >>> sequence = list(range(16))
        >>> abjad.sequence.replace_at(
        ...     sequence,
        ...     ([0, 1, 8, 13], None),
        ...     (['A', 'B', 'C', 'D'], None),
        ... )
        ['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15]

        Replaces every item at even index:

        >>> sequence = list(range(16))
        >>> abjad.sequence.replace_at(
        ...     sequence,
        ...     ([0], 2),
        ...     (['*'], 1),
        ... )
        ['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15]

        Replaces every element at an index congruent to 0 (mod 6) with ``'A'``; replaces
        every element at an index congruent to 2 (mod 6) with ``'B'``:

        >>> sequence = list(range(16))
        >>> abjad.sequence.replace_at(
        ...     sequence,
        ...     ([0], 2),
        ...     (['A', 'B'], 3),
        ... )
        ['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15]

    Returns ``sequence`` type.
    """
    assert isinstance(indices, collections.abc.Sequence)
    assert len(indices) == 2
    index_values, index_period = indices
    assert isinstance(index_values, collections.abc.Sequence)
    index_values = set(index_values)
    assert isinstance(index_period, int | type(None))
    assert isinstance(new_material, collections.abc.Sequence)
    assert len(new_material) == 2
    material_values, material_period = new_material
    assert isinstance(material_values, collections.abc.Sequence)
    material_values = list(material_values)
    assert isinstance(material_period, int | type(None))
    maxsize = sys.maxsize
    if index_period is None:
        index_period = maxsize
    if material_period is None:
        material_period = maxsize
    items = []
    material_index = 0
    for index, item in enumerate(sequence):
        if index % index_period in index_values:
            try:
                cyclic_material_index = material_index % material_period
                material_value = material_values[cyclic_material_index]
                items.append(material_value)
            except IndexError:
                items.append(item)
            material_index += 1
        else:
            items.append(item)
    return type(sequence)(items)


def retain_pattern(sequence, pattern):
    """
    Retains ``sequence`` items at indices matching ``pattern``.

    ..  container:: example

        >>> sequence = list(range(10))

        >>> abjad.sequence.retain_pattern(sequence, abjad.index_all())
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        >>> abjad.sequence.retain_pattern(sequence, abjad.index([2, 3]))
        [2, 3]

        >>> abjad.sequence.retain_pattern(sequence, abjad.index([-2, -3]))
        [7, 8]

        >>> abjad.sequence.retain_pattern(sequence, abjad.index([2, 3], 4))
        [2, 3, 6, 7]

        >>> abjad.sequence.retain_pattern(sequence, abjad.index([-2, -3], 4))
        [0, 3, 4, 7, 8]

        >>> abjad.sequence.retain_pattern(sequence, abjad.index([97, 98, 99]))
        []

        >>> abjad.sequence.retain_pattern(sequence, abjad.index([-97, -98, -99]))
        []

    Returns ``sequence`` type.
    """
    length = len(sequence)
    items = []
    for i, item in enumerate(sequence):
        if pattern.matches_index(i, length):
            items.append(item)
    return type(sequence)(items)


def reverse(sequence, *, recurse: bool = False):
    r"""
    Reverses ``sequence``.

    ..  container:: example

        Reverses sequence:

        >>> sequence = [[1, 2], 3, [4, 5]]

        >>> abjad.sequence.reverse(sequence)
        [[4, 5], 3, [1, 2]]

        Reverses recursively:

        >>> segment_1 = abjad.PitchClassSegment([1, 2])
        >>> pitch = abjad.NumberedPitch(3)
        >>> segment_2 = abjad.PitchClassSegment([4, 5])
        >>> sequence = list([segment_1, pitch, segment_2])

        >>> for item in abjad.sequence.reverse(sequence, recurse=True):
        ...     item
        ...
        PitchClassSegment([5, 4])
        NumberedPitch(3)
        PitchClassSegment([2, 1])

    Returns ``sequence`` type.
    """
    if not recurse:
        return type(sequence)(reversed(sequence))

    def _reverse_helper(item):
        if isinstance(item, collections.abc.Iterable):
            subitems_ = [_reverse_helper(_) for _ in reversed(item)]
            return type(item)(subitems_)
        else:
            return item

    items = _reverse_helper(sequence[:])
    return type(sequence)(items)


def rotate(sequence, n: int = 0):
    r"""
    Rotates ``sequence`` by index ``n``.

    ..  container:: example

        Rotates sequence to the right:

        >>> sequence = list(range(10))

        >>> abjad.sequence.rotate(sequence, n=4)
        [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

        Rotates sequence to the left:

        >>> sequence = list(range(10))

        >>> abjad.sequence.rotate(sequence, n=-3)
        [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

        Rotates sequence to neither the right nor the left:

        >>> sequence = list(range(10))

        >>> abjad.sequence.rotate(sequence, n=0)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Returns ``sequence`` type.
    """
    n = n or 0
    items = []
    if len(sequence):
        n = n % len(sequence)
        for item in sequence[-n : len(sequence)] + sequence[:-n]:
            items.append(item)
    return type(sequence)(items)


def sum_by_sign(sequence, *, sign: typing.Sequence[int] = (-1, 0, 1)):
    """
    Sums consecutive ``sequence`` items by ``sign``.

    >>> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    >>> abjad.sequence.sum_by_sign(sequence)
    [0, -2, 5, -5, 8, -11]

    >>> abjad.sequence.sum_by_sign(sequence, sign=[-1])
    [0, 0, -2, 2, 3, -5, 1, 2, 5, -11]

    >>> abjad.sequence.sum_by_sign(sequence, sign=[0])
    [0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    >>> abjad.sequence.sum_by_sign(sequence, sign=[1])
    [0, 0, -1, -1, 5, -5, 8, -5, -6]

    >>> abjad.sequence.sum_by_sign(sequence, sign=[-1, 0])
    [0, -2, 2, 3, -5, 1, 2, 5, -11]

    >>> abjad.sequence.sum_by_sign(sequence, sign=[-1, 1])
    [0, 0, -2, 5, -5, 8, -11]

    >>> abjad.sequence.sum_by_sign(sequence, sign=[0, 1])
    [0, -1, -1, 5, -5, 8, -5, -6]

    >>> abjad.sequence.sum_by_sign(sequence, sign=[-1, 0, 1])
    [0, -2, 5, -5, 8, -11]

    Sums consecutive negative elements when ``-1`` in ``sign``.

    Sums consecutive zero-valued elements when ``0`` in ``sign``.

    Sums consecutive positive elements when ``1`` in ``sign``.

    Returns ``sequence`` type.
    """
    items = []
    generator = itertools.groupby(sequence, _math.sign)
    for current_sign, group in generator:
        if current_sign in sign:
            items.append(sum(list(group)))
        else:
            for item in group:
                items.append(item)
    return type(sequence)(items)


def truncate(
    sequence,
    *,
    sum_: int | fractions.Fraction | None = None,
    weight: int | fractions.Fraction | None = None,
):
    """
    Truncates ``sequence``.

    >>> sequence = [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

    ..  container:: example

        Truncates sequence to weights ranging from 1 to 10:

        >>> for weight in range(1, 11):
        ...     result = abjad.sequence.truncate(sequence, weight=weight)
        ...     print(weight, result)
        ...
        1 [-1]
        2 [-1, 1]
        3 [-1, 2]
        4 [-1, 2, -1]
        5 [-1, 2, -2]
        6 [-1, 2, -3]
        7 [-1, 2, -3, 1]
        8 [-1, 2, -3, 2]
        9 [-1, 2, -3, 3]
        10 [-1, 2, -3, 4]

        Truncates sequence to sums ranging from 1 to 10:

        >>> for sum_ in range(1, 11):
        ...     result = abjad.sequence.truncate(sequence, sum_=sum_)
        ...     print(sum_, result)
        ...
        1 [-1, 2]
        2 [-1, 2, -3, 4]
        3 [-1, 2, -3, 4, -5, 6]
        4 [-1, 2, -3, 4, -5, 6, -7, 8]
        5 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        6 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        7 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        8 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        9 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
        10 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

        Truncates sequence to zero weight:

        >>> abjad.sequence.truncate(sequence, weight=0)
        []

        Truncates sequence to zero sum:

        >>> abjad.sequence.truncate(sequence, sum_=0)
        []

    Ignores ``sum`` when ``weight`` and ``sum`` are both set.

    Raises value error on negative ``sum``.

    Returns ``sequence`` type.
    """
    if weight is not None:
        assert 0 <= weight, repr(weight)
        items = []
        if 0 < weight:
            total = 0
            for item in sequence:
                total += abs(item)
                if total < weight:
                    items.append(item)
                else:
                    sign = _math.sign(item)
                    trimmed_part = weight - _math.weight(items)
                    trimmed_part *= sign
                    items.append(trimmed_part)
                    break
    elif sum_ is not None:
        assert 0 <= sum_, repr(sum_)
        items = []
        if 0 < sum_:
            total = 0
            for item in sequence:
                total += item
                if total < sum_:
                    items.append(item)
                else:
                    items.append(sum_ - sum(items))
                    break
    return type(sequence)(items)


def weight(sequence) -> typing.Any:
    """
    Gets weight of ``sequence``.

    ..  container:: example

        >>> abjad.sequence.weight([])
        0

        >>> abjad.sequence.weight([1])
        1

        >>> abjad.sequence.weight([1, 2, 3])
        6

        >>> abjad.sequence.weight([1, 2, -3])
        6

        >>> abjad.sequence.weight([-1, -2, -3])
        6

        >>> abjad.sequence.weight([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
        55

        >>> abjad.sequence.weight([[1, -7, -7], [1, -8 -8]])
        32

    """
    weights = []
    for item in sequence:
        if isinstance(item, collections.abc.Iterable):
            weights.append(weight(item))
        else:
            weights.append(abs(item))
    return sum(weights)


def zip(sequences, *, cyclic: bool = False, truncate: bool = True) -> list[tuple]:
    """
    Zips ``sequences``.

    Zips cyclically:

    ..  container:: example

        >>> sequence = [[1, 2, 3], ['a', 'b']]
        >>> for item in abjad.sequence.zip(sequence, cyclic=True):
        ...     item
        ...
        (1, 'a')
        (2, 'b')
        (3, 'a')

        >>> sequence = [[10, 11, 12], [20, 21], [30, 31, 32, 33]]
        >>> for item in abjad.sequence.zip(sequence, cyclic=True):
        ...     item
        ...
        (10, 20, 30)
        (11, 21, 31)
        (12, 20, 32)
        (10, 21, 33)

        Zips without truncation:

        >>> sequence = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
        >>> for item in abjad.sequence.zip(sequence, truncate=False):
        ...     item
        ...
        (1, 11, 21)
        (2, 12, 22)
        (3, 13, 23)
        (4,)

    ..  container:: example

        Zips strictly:

        >>> sequences = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
        >>> for triple in abjad.sequence.zip(sequences):
        ...     triple
        ...
        (1, 11, 21)
        (2, 12, 22)
        (3, 13, 23)

    Returns list of tuples.
    """
    for item in sequences:
        if not isinstance(item, collections.abc.Iterable):
            raise Exception(f"must be iterable: {item!r}.")
    items: list[typing.Any] = []
    if cyclic:
        if not min(len(_) for _ in sequences):
            return items
        maximum_length = max([len(_) for _ in sequences])
        for i in range(maximum_length):
            part = []
            for item in sequences:
                index = i % len(item)
                element = item[index]
                part.append(element)
            items.append(part)
    elif not truncate:
        maximum_length = max([len(_) for _ in sequences])
        for i in range(maximum_length):
            part = []
            for item in sequences:
                try:
                    part.append(item[i])
                except IndexError:
                    pass
            items.append(part)
    elif truncate:
        for item in builtins.zip(*sequences):
            items.append(item)
    result = [tuple(_) for _ in items]
    return result
