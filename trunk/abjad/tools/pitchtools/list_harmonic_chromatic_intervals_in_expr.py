from abjad.tools import sequencetools


def list_harmonic_chromatic_intervals_in_expr(expr):
    '''.. versionadded:: 2.0

    List harmonic chromatic intervals in `expr`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> for interval in sorted(pitchtools.list_harmonic_chromatic_intervals_in_expr(staff)):
        ...     interval
        ...
        HarmonicChromaticInterval(1)
        HarmonicChromaticInterval(2)
        HarmonicChromaticInterval(2)
        HarmonicChromaticInterval(3)
        HarmonicChromaticInterval(4)
        HarmonicChromaticInterval(5)

    Return unordered set.
    '''
    from abjad.tools import pitchtools

    chromatic_intervals = []
    pitches = pitchtools.list_named_chromatic_pitches_in_expr(expr)
    unordered_pitch_pairs = sequencetools.yield_all_unordered_pairs_of_sequence(pitches)
    for first_pitch, second_pitch in unordered_pitch_pairs:
        chromatic_interval_number = abs(first_pitch.numbered_chromatic_pitch) - \
            abs(second_pitch.numbered_chromatic_pitch)
        chromatic_interval = pitchtools.HarmonicChromaticInterval(chromatic_interval_number)
        chromatic_intervals.append(chromatic_interval)

    return chromatic_intervals
