from abjad.tools import mathtools


def calculate_melodic_chromatic_interval(pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic chromatic interval from `pitch_carrier_1` to
    `pitch_carrier_2`::

        >>> pitchtools.calculate_melodic_chromatic_interval(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicChromaticInterval(+14)

    Return melodic chromatic interval.
    '''
    from abjad.tools import pitchtools

    # get pitches
    pitch_1 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
    pitch_2 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)

    # get difference in semitones
    number = abs(pitch_2.numbered_chromatic_pitch) - abs(pitch_1.numbered_chromatic_pitch)

    # change 1.0, 2.0, ... into 1, 2, ...
    number = mathtools.integer_equivalent_number_to_integer(number)

    # make melodic chromatic interval
    mci = pitchtools.MelodicChromaticInterval(number)

    # return melodic chromatic interval
    return mci
