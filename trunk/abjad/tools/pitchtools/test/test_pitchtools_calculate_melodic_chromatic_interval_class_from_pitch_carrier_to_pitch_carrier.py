from abjad import *


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_01():
    '''Ascending intervals greater than an octave.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_02():
    '''Ascending octave.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(12)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_03():
    '''Ascending intervals less than an octave.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_04():
    '''Unison.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(0)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_05():
    '''Descending intervals greater than an octave.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_06():
    '''Descending octave.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-12)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_07():
    '''Descending intervals less than an octave.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_08():
    '''Quartertones.'''

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2.5))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)

    mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9.5))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)
