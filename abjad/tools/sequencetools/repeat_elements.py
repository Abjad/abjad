# -*- encoding: utf-8 -*-


def repeat_elements(sequence, indices=None, period=None, total=1):
    '''Repeats `sequence` elements.

    ..  container:: example

        Repeats elements at indices 1 and 2 a total of three times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     indices=[1, 2], 
            ...     total=3,
            ...     )
            [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, 6, 7, 8, 9]

    ..  container:: example
    
        Repeats elements at indices -1 and -2 a total of three times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     indices=[-1, -2],
            ...     total=3,
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, [8, 8, 8], [9, 9, 9]]

    ..  container:: example

        Repeats elements at indices congruent to 1 and 2 (mod 5) a total of 
        three times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     indices=[1, 2], 
            ...     total=3,
            ...     period=5,
            ...     )
            [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

    ..  container:: example

        Repeats elements at indices congruent to -1 and -2 (mod 5) a total of 
        three times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     indices=[-1, -2], 
            ...     total=3,
            ...     period=5,
            ...     )
            [0, 1, 2, [3, 3, 3], [4, 4, 4], 5, 6, 7, [8, 8, 8], [9, 9, 9]]

    ..  container:: example

        Repeats all elements a total of two times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     total=2,
            ...     )
            [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

    ..  container:: example

        Repeats all elements a total of one time each:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     total=1,
            ...     )
            [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

    ..  container:: example

        Repeats all elements a total of zero times each:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     total=0,
            ...     )
            [[], [], [], [], [], [], [], [], [], []]

    ..  container:: example

        Repeats no elements:

        ::

            >>> sequencetools.repeat_elements(
            ...     range(10), 
            ...     indices=[],
            ...     )
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Returns new object of `sequence` type.
    '''

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

    result = type(sequence)(result)
    return result
