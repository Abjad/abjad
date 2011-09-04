def get_shared_numeric_sign(sequence):
    '''Return ``1`` when all `sequence` elements are positive::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.get_shared_numeric_sign([1, 2, 3])
        1

    Return ``-1`` when all `sequence` elements are negative::

        abjad> mathtools.get_shared_numeric_sign([-1, -2, -3])
        -1

    Return ``0`` on empty `sequence`::

        abjad> mathtools.get_shared_numeric_sign([])
        0

    Otherwise return none::

        abjad> mathtools.get_shared_numeric_sign([1, 2, -3]) is None
        True

    Return ``1``, ``-1``, ``0`` or none.

    .. versionchanged:: 2.0
        renamed ``sequencetools.sign()`` to
        ``mathtools.get_shared_numeric_sign()``.
    '''

    if len(sequence) == 0:
        return 0
    elif all([0 < x for x in sequence]):
        return 1
    elif all([x < 0 for x in sequence]):
        return -1
    else:
        return None
