# -*- encoding: utf-8 -*-


def retain_elements(
    sequence, 
    indices=None,
    period=None, 
    #offset=0,
    ):
    '''Retains `sequence` elements.

    ..  container:: example

        Retains all elements:

        ::

            >>> sequencetools.retain_elements(range(15))
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    ..  container:: example

        Retains elements at indices 2 and 3:

        ::

            >>> sequencetools.retain_elements(
            ...     range(15), 
            ...     indices=[2, 3],
            ...     )
            [2, 3]

    ..  container:: example

        Retains elements at indices -2 and -3:

        ::

            >>> sequencetools.retain_elements(
            ...     range(15), 
            ...     indices=[-2, -3],
            ...     )
            [12, 13]

    ..  container:: example

        Retains elements at indices congruent to 2 or 3 mod 4:

        ::

            >>> sequencetools.retain_elements(
            ...     range(15), 
            ...     indices=[2, 3],
            ...     period=4,
            ...     )
            [2, 3, 6, 7, 10, 11, 14]

    ..  container:: example

        Retains elements at indices congruent to -2 or -3 mod 4:

        ::

            >>> sequencetools.retain_elements(
            ...     range(15), 
            ...     indices=[-2, -3],
            ...     period=4,
            ...     )
            [0, 1, 4, 5, 8, 9, 12, 13]

    ..  container:: example

        Retains no elements:

        ::

            >>> sequencetools.retain_elements(
            ...     range(15), 
            ...     indices=[],
            ...     )
            []

    ..  container:: example

        Retains no elements:

        ::

            >>> sequencetools.retain_elements(
            ...     range(15), 
            ...     indices=[97, 98, 99],
            ...     )
            []

    ..  container:: example

        Retains no elements:

        ::

            >>> sequencetools.retain_elements(
            ...     range(15), 
            ...     indices=[-97, -98, -99],
            ...     )
            []

    Returns sequence elements in the order they appear in `sequence`.

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
        if i % period in indices:
            result.append(element)

    return result
