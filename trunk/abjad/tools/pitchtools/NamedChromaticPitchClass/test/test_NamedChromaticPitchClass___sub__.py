from abjad import *


def test_NamedChromaticPitchClass___sub___01():

    mdi = pitchtools.NamedChromaticPitchClass('c') - pitchtools.NamedChromaticPitchClass('d')
    assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)

    mdi = pitchtools.NamedChromaticPitchClass('d') - pitchtools.NamedChromaticPitchClass('c')
    assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)


def test_NamedChromaticPitchClass___sub___02():

    mdi = pitchtools.NamedChromaticPitchClass('c') - pitchtools.NamedChromaticPitchClass('cf')
    assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 1)

    mdi = pitchtools.NamedChromaticPitchClass('cf') - pitchtools.NamedChromaticPitchClass('c')
    assert mdi == pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 1)
