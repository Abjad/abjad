from abjad import *


def test_MelodicDiatonicInterval___str___01():

    assert str(pitchtools.MelodicDiatonicInterval('perfect', 1)) == 'P1'


def test_MelodicDiatonicInterval___str___02():

    assert str(pitchtools.MelodicDiatonicInterval('augmented', -1)) == '-aug1'

    assert str(pitchtools.MelodicDiatonicInterval('diminished', -2)) == '-dim2'
    assert str(pitchtools.MelodicDiatonicInterval('minor', -2)) == '-m2'
    assert str(pitchtools.MelodicDiatonicInterval('major', -2)) == '-M2'
    assert str(pitchtools.MelodicDiatonicInterval('augmented', -2)) == '-aug2'

    assert str(pitchtools.MelodicDiatonicInterval('diminished', -3)) == '-dim3'
    assert str(pitchtools.MelodicDiatonicInterval('minor', -3)) == '-m3'
    assert str(pitchtools.MelodicDiatonicInterval('major', -3)) == '-M3'
    assert str(pitchtools.MelodicDiatonicInterval('augmented', -3)) == '-aug3'


def test_MelodicDiatonicInterval___str___03():

    assert str(pitchtools.MelodicDiatonicInterval('augmented', 1)) == '+aug1'

    assert str(pitchtools.MelodicDiatonicInterval('diminished', 2)) == '+dim2'
    assert str(pitchtools.MelodicDiatonicInterval('minor', 2)) == '+m2'
    assert str(pitchtools.MelodicDiatonicInterval('major', 2)) == '+M2'
    assert str(pitchtools.MelodicDiatonicInterval('augmented', 2)) == '+aug2'

    assert str(pitchtools.MelodicDiatonicInterval('diminished', 3)) == '+dim3'
    assert str(pitchtools.MelodicDiatonicInterval('minor', 3)) == '+m3'
    assert str(pitchtools.MelodicDiatonicInterval('major', 3)) == '+M3'
    assert str(pitchtools.MelodicDiatonicInterval('augmented', 3)) == '+aug3'
