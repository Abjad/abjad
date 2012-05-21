from abjad import *


def testMelodicObjectDiatonicIntervalClass___init___01():
    '''Unisons and octaves are treated differently.'''

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', -15)
    assert str(mdic) == '-P8'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', -8)
    assert str(mdic) == '-P8'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', 8)
    assert str(mdic) == '+P8'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', 15)
    assert str(mdic) == '+P8'


def testMelodicObjectDiatonicIntervalClass___init___02():
    '''Unisons and octaves are treated differently.'''

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', -1)
    assert str(mdic) == 'P1'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', 1)
    assert str(mdic) == 'P1'
