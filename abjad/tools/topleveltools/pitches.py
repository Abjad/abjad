def pitches(operator, pitches):
    r'''Pitch inequality factory function.

    ..  container:: example

        >>> inequality = abjad.pitches('&', 'C4')
        >>> abjad.f(inequality)
        abjad.PitchInequality(
            operator_string='&',
            pitches=abjad.PitchSet(
                [0]
                ),
            )

        >>> inequality = abjad.pitches('&', 'C4 E4')
        >>> abjad.f(inequality)
        abjad.PitchInequality(
            operator_string='&',
            pitches=abjad.PitchSet(
                [0, 4]
                ),
            )

    Returns pitch inequality.
    '''
    import abjad
    return abjad.PitchInequality(operator, pitches)
