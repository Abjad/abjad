# -*- coding: utf-8 -*-
import collections


def remove_elements(
    sequence,
    indices=None,
    period=None,
    ):
    '''Removes `sequence` elements at `indices`.

    ..  container:: example

        Sequence for examples:

        ::

            >>> sequence = list(range(15))

    ..  container:: example

        **Example 1.** Removes all elements:

        ::

            >>> sequencetools.remove_elements(sequence)
            []

    ..  container:: example

        **Example 2.** Removes elements and indices 2 and 3:

        ::

            >>> sequencetools.remove_elements(
            ...     sequence,
            ...     indices=[2, 3],
            ...     )
            [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        **Example 3.** Removes elements and indices -2 and -3:

        ::

            >>> sequencetools.remove_elements(
            ...     sequence,
            ...     indices=[-2, -3],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14]

    ..  container:: example

        **Example 4.** Removes elements and indices 2 and 3 (mod 4):

        ::

            >>> sequencetools.remove_elements(
            ...     sequence,
            ...     indices=[2, 3],
            ...     period=4,
            ...     )
            [0, 1, 4, 5, 8, 9, 12, 13]

    ..  container:: example

        **Example 5.** Removes elements at indices -2 and -3 (mod 4):

        ::

            >>> sequencetools.remove_elements(
            ...     sequence,
            ...     indices=[-2, -3],
            ...     period=4,
            ...     )
            [2, 3, 6, 7, 10, 11, 14]

    ..  container:: example

        **Example 6.** Removes no elements:

        ::

            >>> sequencetools.remove_elements(
            ...     sequence,
            ...     indices=[],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        **Example 7.** Removes no elements:

        ::

            >>> sequencetools.remove_elements(
            ...     sequence,
            ...     indices=[97, 98, 99],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        **Example 8.** Removes no elements:

        ::

            >>> sequencetools.remove_elements(
            ...     sequence,
            ...     indices=[-97, -98, -99],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        **Example 9.** Removes tuple elements at indices -2 and -3 (mod 4):

        ::

            >>> sequencetools.remove_elements(
            ...     tuple(sequence),
            ...     indices=[-2, -3],
            ...     period=4,
            ...     )
            (2, 3, 6, 7, 10, 11, 14)

    Returns elements in the order they appear in `sequence`.

    Returns new object of `sequence` type.
    '''
    
    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    result = []

    length = len(sequence)
    period = period or length

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

    for i, element in enumerate(sequence):
        if i % period not in indices:
            result.append(element)

    result = sequence_type(result)

    return result
