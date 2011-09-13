from abjad.tools.pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch import calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch


def calculate_harmonic_counterpoint_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
    pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate harmonic counterpoint interval-class from `pitch_carrier_1` to
    `pitch_carrier_2`::

        abjad> pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        HarmonicCounterpointIntervalClass(2)

    Return harmonic counterpoint interval-class.

    .. versionchanged:: 2.0
        renamed ``pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_pchromatic_pitch_to_named_chromatic_pitch()`` to
        ``pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch()``.
    '''

    # get melodic diatonic interval
    mdi = calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(pitch_carrier_1, pitch_carrier_2)

    # return harmonic counterpoint interval-class
    return mdi.harmonic_counterpoint_interval.harmonic_counterpoint_interval_class
