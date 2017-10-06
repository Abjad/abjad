def length(operator, length):
    r'''Length inequality factory function.

    ..  container:: example

        >>> inequality = abjad.length('==', 1)
        >>> abjad.f(inequality)
        abjad.LengthInequality(
            operator_string='==',
            length=1,
            )

        >>> inequality = abjad.length('<=', 4)
        >>> abjad.f(inequality)
        abjad.LengthInequality(
            operator_string='<=',
            length=4,
            )

    Returns length inequality.
    '''
    import abjad
    return abjad.LengthInequality(operator, length)
