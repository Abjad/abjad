from abjad.tools.pitchtools.diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval import diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier


def calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
    pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic diatonic interval from `pitch_carrier_1` to
    `pitch_carrier_2`::

        abjad> pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicDiatonicInterval('+M9')

    Return melodic diatonic interval.
    '''

    pitch_1 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
    pitch_2 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)

    degree_1 = abs(pitch_1.numbered_diatonic_pitch)
    degree_2 = abs(pitch_2.numbered_diatonic_pitch)

    diatonic_interval_number = abs(degree_1 - degree_2) + 1

    chromatic_interval_number = abs(abs(pitch_1.numbered_chromatic_pitch) -
        abs(pitch_2.numbered_chromatic_pitch))

    absolute_diatonic_interval = \
        diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval(
        diatonic_interval_number, chromatic_interval_number)

    if pitch_2 < pitch_1:
        diatonic_interval = -absolute_diatonic_interval
    else:
        diatonic_interval = absolute_diatonic_interval

    return diatonic_interval
