from abjad import *


def test_MelodicDiatonicIntervalClass___eq___01():

    mdic_1 = pitchtools.MelodicDiatonicIntervalClass('perfect', 1)
    mdic_2 = pitchtools.MelodicDiatonicIntervalClass('perfect', -1)

    assert mdic_1 == mdic_2
    assert mdic_2 == mdic_1

    assert not mdic_1 != mdic_2
    assert not mdic_2 != mdic_2

    assert not mdic_1 is mdic_2
    assert not mdic_2 is mdic_1


def test_MelodicDiatonicIntervalClass___eq___02():

    mdic_1 = pitchtools.MelodicDiatonicIntervalClass('perfect', 2)
    mdic_2 = pitchtools.MelodicDiatonicIntervalClass('perfect', 9)

    assert mdic_1 == mdic_2
    assert mdic_2 == mdic_1

    assert not mdic_1 != mdic_2
    assert not mdic_2 != mdic_2

    assert not mdic_1 is mdic_2
    assert not mdic_2 is mdic_1


def test_MelodicDiatonicIntervalClass___eq___03():

    mdic_1 = pitchtools.MelodicDiatonicIntervalClass('perfect', -2)
    mdic_2 = pitchtools.MelodicDiatonicIntervalClass('perfect', -9)

    assert mdic_1 == mdic_2
    assert mdic_2 == mdic_1

    assert not mdic_1 != mdic_2
    assert not mdic_2 != mdic_2

    assert not mdic_1 is mdic_2
    assert not mdic_2 is mdic_1
