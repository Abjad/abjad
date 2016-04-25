# -*- coding: utf-8 -*-
import collections


def splice_between_elements(
    sequence,
    new_elements,
    overhang=(0, 0),
    ):
    '''Splices copies of `new_elements` between each of the elements
    of `sequence`.

    ::

        >>> sequence = [0, 1, 2, 3, 4]
        >>> new_elements = ['A', 'B']

    ..  container:: example

        **Example 1.** Splices characters between integers:

        ::

            >>> sequencetools.splice_between_elements(sequence, new_elements)
            [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    ..  container:: example

        **Example 2.** Splices copies of `new_elements` between each of the
        elements of `sequence` and after the last element of `sequence`:

        ::

            >>> sequencetools.splice_between_elements(
            ...     sequence, new_elements, overhang=(0, 1))
            [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

    ..  container:: example

        **Example 3.** Splices copies of `new_elements` before the first
        element of `sequence` and between each of the other elements of
        `sequence`:

        ::

            >>> sequencetools.splice_between_elements(
            ...     sequence, new_elements, overhang=(1, 0))
            ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    ..  container:: example

        **Example 4.** Splices copies of `new_elements` before the first
        element of `sequence`, after the last element of `sequence` and between
        each of the other elements of `sequence`:

        ::

            >>> sequencetools.splice_between_elements(
            ...     sequence, new_elements, overhang=(1, 1))
            ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    result = []

    if overhang[0] == 1:
        result.extend(new_elements[:])

    for element in sequence[:-1]:
        result.append(element)
        result.extend(new_elements[:])

    result.append(sequence[-1])

    if overhang[-1] == 1:
        result.extend(new_elements)

    result = sequence_type(result)
    return result
