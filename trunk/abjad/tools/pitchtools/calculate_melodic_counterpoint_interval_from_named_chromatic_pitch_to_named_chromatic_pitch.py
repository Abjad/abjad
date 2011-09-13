from abjad.tools.pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch import calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch


def calculate_melodic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
    pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic counterpoint interval `pitch_carrier_1` to
    `pitch_carrier_2`::

        abjad> pitchtools.calculate_melodic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicCounterpointInterval(+9)

    Return melodic counterpoint interval.
    '''

    # get melodic diatonic interval
    mdi = calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitch_carrier_1, pitch_carrier_2)

    # return melodic counterpoint interval
    return mdi.melodic_counterpoint_interval
