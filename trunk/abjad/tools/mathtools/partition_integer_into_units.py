from abjad.tools.mathtools.sign import sign


def partition_integer_into_units(n):
    '''Partition positive integer into units::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.partition_integer_into_units(6)
        [1, 1, 1, 1, 1, 1]

    Partition negative integer into units::

        abjad> mathtools.partition_integer_into_units(-5)
        [-1, -1, -1, -1, -1]

    Partition ``0`` into units::

        abjad> mathtools.partition_integer_into_units(0)
        []

    Return list of zero or more parts with absolute value equal to ``1``.
    '''

    return abs(n) * [sign(n) * 1]
