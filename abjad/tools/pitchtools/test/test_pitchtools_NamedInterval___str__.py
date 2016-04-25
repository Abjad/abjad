# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___str___01():

    assert str(pitchtools.NamedInterval('perfect', 1)) == 'P1'


def test_pitchtools_NamedInterval___str___02():

    assert str(pitchtools.NamedInterval('augmented', -1)) == '-aug1'

    assert str(pitchtools.NamedInterval('diminished', -2)) == '-dim2'
    assert str(pitchtools.NamedInterval('minor', -2)) == '-m2'
    assert str(pitchtools.NamedInterval('major', -2)) == '-M2'
    assert str(pitchtools.NamedInterval('augmented', -2)) == '-aug2'

    assert str(pitchtools.NamedInterval('diminished', -3)) == '-dim3'
    assert str(pitchtools.NamedInterval('minor', -3)) == '-m3'
    assert str(pitchtools.NamedInterval('major', -3)) == '-M3'
    assert str(pitchtools.NamedInterval('augmented', -3)) == '-aug3'


def test_pitchtools_NamedInterval___str___03():

    assert str(pitchtools.NamedInterval('augmented', 1)) == '+aug1'

    assert str(pitchtools.NamedInterval('diminished', 2)) == '+dim2'
    assert str(pitchtools.NamedInterval('minor', 2)) == '+m2'
    assert str(pitchtools.NamedInterval('major', 2)) == '+M2'
    assert str(pitchtools.NamedInterval('augmented', 2)) == '+aug2'

    assert str(pitchtools.NamedInterval('diminished', 3)) == '+dim3'
    assert str(pitchtools.NamedInterval('minor', 3)) == '+m3'
    assert str(pitchtools.NamedInterval('major', 3)) == '+M3'
    assert str(pitchtools.NamedInterval('augmented', 3)) == '+aug3'
