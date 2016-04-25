# -*- coding: utf-8 -*-
import collections


def repeat_elements(sequence, indices=None, period=None, total=1):
    '''Repeats `sequence` elements.

    ..  container:: example

        **Example 1.** Repeats elements at indices 1 and 2 a total of three
        times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     indices=[1, 2],
            ...     total=3,
            ...     )
            [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, 6, 7, 8, 9]

    ..  container:: example

        **Example 2.** Repeats elements at indices -1 and -2 a total of three
        times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     indices=[-1, -2],
            ...     total=3,
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, [8, 8, 8], [9, 9, 9]]

    ..  container:: example

        **Example 3.** Repeats elements at indices congruent to 1 and 2 (mod 5)
        a total of three times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     indices=[1, 2],
            ...     total=3,
            ...     period=5,
            ...     )
            [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

    ..  container:: example

        **Example 4.** Repeats elements at indices congruent to -1 and -2 (mod
        5) a total of three times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     indices=[-1, -2],
            ...     total=3,
            ...     period=5,
            ...     )
            [0, 1, 2, [3, 3, 3], [4, 4, 4], 5, 6, 7, [8, 8, 8], [9, 9, 9]]

    ..  container:: example

        **Example 5.** Repeats all elements a total of two times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     total=2,
            ...     )
            [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

    ..  container:: example

        **Example 6.** Repeats all elements a total of one time each:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     total=1,
            ...     )
            [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

    ..  container:: example

        **Example 7.** Repeats all elements a total of zero times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     total=0,
            ...     )
            [[], [], [], [], [], [], [], [], [], []]

    ..  container:: example

        **Example 8.** Repeats no elements:

        ::

            >>> sequencetools.repeat_elements(
            ...     list(range(10)),
            ...     indices=[],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

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

    result = []

    for i, element in enumerate(sequence):
        if i % period in indices:
            result.append(total * [element])
        else:
            result.append(element)

    result = sequence_type(result)
    return result
