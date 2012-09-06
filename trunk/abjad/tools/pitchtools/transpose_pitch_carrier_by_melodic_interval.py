def transpose_pitch_carrier_by_melodic_interval(pitch_carrier, melodic_interval):
    '''.. versionadded:: 2.0

    Transpose `pitch_carrier` by diatonic `melodic_interval`::

        >>> chord = Chord("<c' e' g'>4")

    ::

        >>> pitchtools.transpose_pitch_carrier_by_melodic_interval(chord, '+m2')
        Chord("<df' f' af'>4")

    Transpose `pitch_carrier` by chromatic `melodic_interval`::

        >>> chord = Chord("<c' e' g'>4")

    ::

        >>> pitchtools.transpose_pitch_carrier_by_melodic_interval(chord, 1)
        Chord("<cs' f' af'>4")

    Return non-pitch-carrying input unchaged::

        >>> rest = Rest('r4')

    ::

        >>> pitchtools.transpose_pitch_carrier_by_melodic_interval(rest, 1)
        Rest('r4')

    Return `pitch_carrier`.
    '''
    from abjad.tools import pitchtools
    from abjad.tools.pitchtools._transpose_pitch_carrier_by_melodic_chromatic_interval import \
        _transpose_pitch_carrier_by_melodic_chromatic_interval
    from abjad.tools.pitchtools._transpose_pitch_carrier_by_melodic_diatonic_interval import \
        _transpose_pitch_carrier_by_melodic_diatonic_interval

    if isinstance(melodic_interval, (pitchtools.MelodicDiatonicInterval, str)):
        melodic_interval = pitchtools.MelodicDiatonicInterval(melodic_interval)
        return _transpose_pitch_carrier_by_melodic_diatonic_interval(pitch_carrier, melodic_interval)
    else:
        melodic_interval = pitchtools.MelodicChromaticInterval(melodic_interval)
        return _transpose_pitch_carrier_by_melodic_chromatic_interval(pitch_carrier, melodic_interval)
