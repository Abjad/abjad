from abjad import *


def test_NamedChromaticPitch___sub___01():

    pitch = pitchtools.NamedChromaticPitch(12)
    diatonic_interval = pitchtools.MelodicDiatonicInterval('diminished', 3)

    assert pitch - diatonic_interval == pitchtools.NamedChromaticPitch('as', 4)


def test_NamedChromaticPitch___sub___02():

    pitch = pitchtools.NamedChromaticPitch(12)
    chromatic_interval = pitchtools.MelodicChromaticInterval(2)

    assert pitch - chromatic_interval == pitchtools.NamedChromaticPitch('bf', 4)


def test_NamedChromaticPitch___sub___03():

    pitch_1 = pitchtools.NamedChromaticPitch(12)
    pitch_2 = pitchtools.NamedChromaticPitch(10)

    assert pitch_1 - pitch_2 == pitchtools.MelodicDiatonicInterval('major', -2)
    assert pitch_2 - pitch_1 == pitchtools.MelodicDiatonicInterval('major', 2)
