def weight(sequence):
    '''Sum of the absolute value of the elements in `sequence`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.weight([-1, -2, 3, 4, 5])
        15

    Return nonnegative integer.

    .. versionchanged:: 2.0
        renamed ``sequencetools.weight()`` to
        ``mathtools.weight()``.
    '''

    return sum([abs(element) for element in sequence])
