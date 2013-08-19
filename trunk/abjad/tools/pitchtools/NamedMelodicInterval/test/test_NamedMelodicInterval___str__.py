# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___str___01():

    assert str(pitchtools.NamedMelodicInterval('perfect', 1)) == 'P1'


def test_NamedMelodicInterval___str___02():

    assert str(pitchtools.NamedMelodicInterval('augmented', -1)) == '-aug1'

    assert str(pitchtools.NamedMelodicInterval('diminished', -2)) == '-dim2'
    assert str(pitchtools.NamedMelodicInterval('minor', -2)) == '-m2'
    assert str(pitchtools.NamedMelodicInterval('major', -2)) == '-M2'
    assert str(pitchtools.NamedMelodicInterval('augmented', -2)) == '-aug2'

    assert str(pitchtools.NamedMelodicInterval('diminished', -3)) == '-dim3'
    assert str(pitchtools.NamedMelodicInterval('minor', -3)) == '-m3'
    assert str(pitchtools.NamedMelodicInterval('major', -3)) == '-M3'
    assert str(pitchtools.NamedMelodicInterval('augmented', -3)) == '-aug3'


def test_NamedMelodicInterval___str___03():

    assert str(pitchtools.NamedMelodicInterval('augmented', 1)) == '+aug1'

    assert str(pitchtools.NamedMelodicInterval('diminished', 2)) == '+dim2'
    assert str(pitchtools.NamedMelodicInterval('minor', 2)) == '+m2'
    assert str(pitchtools.NamedMelodicInterval('major', 2)) == '+M2'
    assert str(pitchtools.NamedMelodicInterval('augmented', 2)) == '+aug2'

    assert str(pitchtools.NamedMelodicInterval('diminished', 3)) == '+dim3'
    assert str(pitchtools.NamedMelodicInterval('minor', 3)) == '+m3'
    assert str(pitchtools.NamedMelodicInterval('major', 3)) == '+M3'
    assert str(pitchtools.NamedMelodicInterval('augmented', 3)) == '+aug3'
