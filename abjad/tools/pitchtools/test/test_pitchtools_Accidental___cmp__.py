# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental___cmp___01():
    r'''Accidentals equal by string compare equally.
    '''
    k1, k2 = pitchtools.Accidental('s'), pitchtools.Accidental('s')
    assert      k1 == k2
    assert not k1 != k2
    assert not k1 >  k2
    assert      k1 >= k2
    assert not k1 <  k2
    assert      k1 <= k2


def test_pitchtools_Accidental___cmp___02():
    r'''Accidentals unequal by string compare unequally.
    '''
    k1, k2 = pitchtools.Accidental('s'), pitchtools.Accidental('f')
    assert not k1 == k2
    assert      k1 != k2
    assert      k1 >  k2
    assert      k1 >= k2
    assert not k1 <  k2
    assert not k1 <= k2


def test_pitchtools_Accidental___cmp___03():
    r'''No accidental and forced natural compare in a special way.
    '''
    k1, k2 = pitchtools.Accidental(''), pitchtools.Accidental('!')
    assert not k1 == k2
    assert      k1 != k2
    assert not k1 >  k2
    assert      k1 >= k2
    assert not k1 <  k2
    assert      k1 <= k2
