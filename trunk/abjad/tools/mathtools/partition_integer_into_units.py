def partition_integer_into_units(n):
    '''Partition positive integer into units::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.partition_integer_into_units(6)
        [1, 1, 1, 1, 1, 1]

    Partition negative integer into units::

        >>> mathtools.partition_integer_into_units(-5)
        [-1, -1, -1, -1, -1]

    Partition ``0`` into units::

        >>> mathtools.partition_integer_into_units(0)
        []

    Return list of zero or more parts with absolute value equal to ``1``.
    '''
    from abjad.tools import mathtools

    result = abs(n) * [mathtools.sign(n) * 1]

    return result
