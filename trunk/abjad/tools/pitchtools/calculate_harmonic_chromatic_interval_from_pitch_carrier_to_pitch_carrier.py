from abjad.tools.pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier import calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier


def calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
    pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate harmonic chromatic interval from `pitch_carrier_1` to
    `pitch_carrier_2`::

        abjad> pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        HarmonicChromaticInterval(14)

    Return harmonic chromatic interval.
    '''

    # get melodic chromatic interval
    mci = calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(
        pitch_carrier_1, pitch_carrier_2)

    # return harmonic chromatic interval
    return mci.harmonic_chromatic_interval
