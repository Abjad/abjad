from abjad.tools import mathtools
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier


def calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
    pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic chromatic interval from `pitch_carrier_1` to
    `pitch_carrier_2`::

        abjad> pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicChromaticInterval(+14)

    Return melodic chromatic interval.
    '''

    # get pitches
    pitch_1 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
    pitch_2 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)

    # get difference in semitones
    number = abs(pitch_2.numbered_chromatic_pitch) - abs(pitch_1.numbered_chromatic_pitch)

    # change 1.0, 2.0, ... into 1, 2, ...
    number = mathtools.integer_equivalent_number_to_integer(number)

    # make melodic chromatic interval
    mci = MelodicChromaticInterval(number)

    # return melodic chromatic interval
    return mci
