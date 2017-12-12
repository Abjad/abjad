def duration(operator, duration, preprolated=None):
    r'''Duration inequality factory function.

    ..  container:: example

        >>> inequality = abjad.duration('==', (1, 16))
        >>> abjad.f(inequality)
        abjad.DurationInequality(
            operator_string='==',
            duration=abjad.Duration(1, 16),
            )

        >>> inequality = abjad.duration('<=', (1, 4))
        >>> abjad.f(inequality)
        abjad.DurationInequality(
            operator_string='<=',
            duration=abjad.Duration(1, 4),
            )

    Returns duration inequality.
    '''
    import abjad
    return abjad.DurationInequality(
        operator,
        duration,
        preprolated=preprolated,
        )
