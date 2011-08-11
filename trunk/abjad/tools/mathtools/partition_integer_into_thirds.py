def partition_integer_into_thirds(n, smallest = 'middle', biggest = 'middle'):
    '''Partition positive integer `n` into ``left, middle, right`` parts.

    When ``n % 3 == 0``, ``left == middle == right``::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.partition_integer_into_thirds(9)
        (3, 3, 3)

    When ``n % 3 == 1``, set biggest part to `biggest`::

        abjad> mathtools.partition_integer_into_thirds(10, biggest = 'left')
        (4, 3, 3)
        abjad> mathtools.partition_integer_into_thirds(10, biggest = 'middle')
        (3, 4, 3)
        abjad> mathtools.partition_integer_into_thirds(10, biggest = 'right')
        (3, 3, 4)

    When ``n % 3 == 2``, set smallest part to `smallest`::

        abjad> mathtools.partition_integer_into_thirds(11, smallest = 'left')
        (3, 4, 4)
        abjad> mathtools.partition_integer_into_thirds(11, smallest = 'middle')
        (4, 3, 4)
        abjad> mathtools.partition_integer_into_thirds(11, smallest = 'right')
        (4, 4, 3)

    Raise type error on noninteger `n`.

    Raise value error on nonpositive `n`.

    Return triple of positive integers.
    '''

    if not isinstance(n, int):
        raise TypeError

    if n <= 0:
        raise ValueError

    assert smallest in ('left', 'middle', 'right')
    assert biggest in ('left', 'middle', 'right')

    small = int(n / 3)
    big = small + 1

    if n % 3 == 0:
        return small, small, small
    elif n % 3 == 1:
        if biggest == 'left':
            return big, small, small
        elif biggest == 'middle':
            return small, big, small
        elif biggest == 'right':
            return small, small, big
    elif n % 3 == 2:
        if smallest == 'left':
            return small, big, big
        elif smallest == 'middle':
            return big, small, big
        elif smallest == 'right':
            return big, big, small
    else:
        raise ValueError
