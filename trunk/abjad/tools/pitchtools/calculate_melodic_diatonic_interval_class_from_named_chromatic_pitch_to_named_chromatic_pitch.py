from abjad.tools.pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch import calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch


def calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(
    pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic diatonic interval-class from `pitch_carrier_1` to
    `pitch_carrier_2`::

        abjad> pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicDiatonicIntervalClass('+M2')

    Return melodic diatonic interval-class.
    '''

    # get melodic diatonic interval
    mdi = calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
        pitch_carrier_1, pitch_carrier_2)

    # return melodic diatonic interval-class
    return mdi.melodic_diatonic_interval_class
