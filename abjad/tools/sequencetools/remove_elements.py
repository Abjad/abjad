# -*- encoding: utf-8 -*-


def remove_elements(
    sequence, 
    indices=None,
    period=None, 
    ):
    '''Removes `sequence` elements at `indices`.

    ..  container:: example

        Removes all elements:

        ::

            >>> sequencetools.remove_elements(range(15))
            []

    ..  container:: example

        Removes elements and indices 2 and 3:

        ::

            >>> sequencetools.remove_elements(
            ...     range(15),
            ...     indices=[2, 3],
            ...     )
            [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        Removes elements and indices -2 and -3:

        ::

            >>> sequencetools.remove_elements(
            ...     range(15),
            ...     indices=[-2, -3],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14]

    ..  container:: example

        Removes elements and indices 2 and 3 (mod 4):

        ::

            >>> sequencetools.remove_elements(
            ...     range(15),
            ...     indices=[2, 3],
            ...     period=4,
            ...     )
            [0, 1, 4, 5, 8, 9, 12, 13]

    ..  container:: example

        Removes elements and indices -2 and -3 (mod 4):

        ::

            >>> sequencetools.remove_elements(
            ...     range(15),
            ...     indices=[-2, -3],
            ...     period=4,
            ...     )
            [2, 3, 6, 7, 10, 11, 14]

    ..  container:: example

        Removes no elements:

        ::

            >>> sequencetools.remove_elements(
            ...     range(15),
            ...     indices=[],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        Removes no elements:

        ::

            >>> sequencetools.remove_elements(
            ...     range(15),
            ...     indices=[97, 98, 99],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        Removes no elements:

        ::

            >>> sequencetools.remove_elements(
            ...     range(15),
            ...     indices=[-97, -98, -99],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    Returns elements in the order they appear in `sequence`.

    Returns list.
    '''

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

    return result
