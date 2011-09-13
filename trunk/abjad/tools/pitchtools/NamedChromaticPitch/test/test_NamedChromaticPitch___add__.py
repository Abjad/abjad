from abjad import *


def test_NamedChromaticPitch___add___01():

    pitch = pitchtools.NamedChromaticPitch(12)
    diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 2)

    assert pitch + diatonic_interval == pitchtools.NamedChromaticPitch('df', 5)


def test_NamedChromaticPitch___add___02():

    pitch = pitchtools.NamedChromaticPitch(12)
    chromatic_interval = pitchtools.MelodicChromaticInterval(1)

    assert pitch + chromatic_interval == pitchtools.NamedChromaticPitch('cs', 5)
