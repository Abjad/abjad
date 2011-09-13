def duration_pair_to_prolation_string(pair):
    '''.. versionadded:: 2.0

    Change positive integer duration `pair` to colon-separated prolation string::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.duration_pair_to_prolation_string((2, 3))
        '3:2'

    Return string.
    '''

    numerator, denominator = pair
    if not 0 < numerator:
        raise ValueError('numerator must be positive.')
    if not 0 < denominator:
        raise ValueError('denominator must be positive.')

    prolation_string = '%s:%s' % (denominator, numerator)

    return prolation_string
