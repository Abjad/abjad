# -*- coding: utf-8 -*-
import collections
from abjad.tools import mathtools


def split_sequence(sequence, weights, cyclic=False, overhang=False):
    '''Splits sequence by weights.

    ..  container:: example

        **Example 1.** Splits sequence cyclically by weights with overhang:

        ::

            >>> sequencetools.split_sequence(
            ...     (10, -10, 10, -10),
            ...     (3, 15, 3),
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            ((3,), (7, -8), (-2, 1), (3,), (6, -9), (-1,))

    ..  container:: example

        **Example 2.** Splits sequence cyclically by weights without overhang:

        ::

            >>> sequencetools.split_sequence(
            ...     (10, -10, 10, -10),
            ...     (3, 15, 3),
            ...     cyclic=True,
            ...     overhang=False,
            ...     )
            ((3,), (7, -8), (-2, 1), (3,), (6, -9))

    ..  container:: example

        **Example 3.** Splits sequence once by weights with overhang:

        ::

            >>> sequencetools.split_sequence(
            ...     (10, -10, 10, -10),
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=True,
            ...     )
            ((3,), (7, -8), (-2, 1), (9, -10))

    ..  container:: example

        **Example 4.** Splits sequence once by weights without overhang:

        ::

            >>> sequencetools.split_sequence(
            ...     (10, -10, 10, -10),
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            ((3,), (7, -8), (-2, 1))

    ..  container:: example

        **Example 5.** Splits list once by weights without overhang:

        ::

            >>> sequencetools.split_sequence(
            ...     [10, -10, 10, -10],
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            [[3], [7, -8], [-2, 1]]

    Returns new object of `sequence` type with elements also of `sequence`
    type.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    result = []
    current_index = 0
    current_piece = []

    if cyclic:
        weights = sequencetools.repeat_sequence_to_weight(
            weights,
            mathtools.weight(sequence),
            allow_total=Less,
            )

    for weight in weights:
        current_piece_weight = mathtools.weight(current_piece)
        while current_piece_weight < weight:
            current_piece.append(sequence[current_index])
            current_index += 1
            current_piece_weight = mathtools.weight(current_piece)
        if current_piece_weight == weight:
            current_piece = type(sequence)(current_piece)
            result.append(current_piece)
            current_piece = []
        elif weight < current_piece_weight:
            overage = current_piece_weight - weight
            current_last_element = current_piece.pop(-1)
            needed = abs(current_last_element) - overage
            needed *= mathtools.sign(current_last_element)
            current_piece.append(needed)
            current_piece = type(sequence)(current_piece)
            result.append(current_piece)
            overage *= mathtools.sign(current_last_element)
            current_piece = [overage]

    if overhang:
        last_piece = current_piece
        last_piece.extend(sequence[current_index:])
        if last_piece:
            last_piece = type(sequence)(last_piece)
            result.append(last_piece)

    result = sequence_type(result)
    return result
