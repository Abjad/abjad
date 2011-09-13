from abjad import *


def test_Accidental___cmp___01():
    '''Accidentals equal by string compare equally.'''
    k1, k2 = pitchtools.Accidental('s'), pitchtools.Accidental('s')
    assert      k1 == k2
    assert not k1 != k2
    assert not k1 >  k2
    assert      k1 >= k2
    assert not k1 <  k2
    assert      k1 <= k2


def test_Accidental___cmp___02():
    '''Accidentals unequal by string compare unequally.'''
    k1, k2 = pitchtools.Accidental('s'), pitchtools.Accidental('f')
    assert not k1 == k2
    assert      k1 != k2
    assert      k1 >  k2
    assert      k1 >= k2
    assert not k1 <  k2
    assert not k1 <= k2


def test_Accidental___cmp___03():
    '''No accidental and forced natural compare in a special way.'''
    k1, k2 = pitchtools.Accidental(''), pitchtools.Accidental('!')
    assert not k1 == k2
    assert      k1 != k2
    assert not k1 >  k2
    assert      k1 >= k2
    assert not k1 <  k2
    assert      k1 <= k2
