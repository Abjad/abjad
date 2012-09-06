from abjad.tools import sequencetools


def expr_to_melodic_chromatic_interval_segment(expr):
    '''.. versionadded:: 2.0

    Change `expr` to melodic chromatic interval segment::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> pitchtools.expr_to_melodic_chromatic_interval_segment(staff)
        MelodicChromaticIntervalSegment(+2, +2, +1, +2, +2, +2, +1)

    Return melodic chromatic interval segment.
    '''
    from abjad.tools import pitchtools

    pitches = pitchtools.list_named_chromatic_pitches_in_expr(expr)
    mcis = []
    for left, right in sequencetools.iterate_sequence_pairwise_strict(pitches):
        mci = pitchtools.calculate_melodic_chromatic_interval(left, right)
        mcis.append(mci)

    return pitchtools.MelodicChromaticIntervalSegment(mcis)
