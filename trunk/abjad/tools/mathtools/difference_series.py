def difference_series(sequence):
    '''Difference series of `sequence`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.difference_series([1, 1, 2, 3, 5, 5, 6])
        [0, 1, 1, 2, 0, 1]

    Return list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.difference_series()`` to
        ``mathtools.difference_series()``.
    '''

    result = []

    for i, n in enumerate(sequence[1:]):
        #yield n - l[i]
        result.append(n - sequence[i])

    return result
