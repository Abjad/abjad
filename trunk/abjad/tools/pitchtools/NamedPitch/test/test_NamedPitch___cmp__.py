# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedPitch___cmp___01():
    r'''Referentially equal pitches compare equally.
    '''
    pitch_1 = pitchtools.NamedPitch('fs', 4)
    assert      pitch_1 == pitch_1
    assert not pitch_1 != pitch_1
    assert not pitch_1 >  pitch_1
    assert      pitch_1 >= pitch_1
    assert not pitch_1 <  pitch_1
    assert      pitch_1 <= pitch_1


def test_NamedPitch___cmp___02():
    r'''Pitches equal by name, accidental and octave compare equally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('fs', 4)
    assert      pitch_1 == pitch_2
    assert not pitch_1 != pitch_2
    assert not pitch_1 >  pitch_1
    assert      pitch_1 >= pitch_1
    assert not pitch_1 <  pitch_1
    assert      pitch_1 <= pitch_1


def test_NamedPitch___cmp___03():
    r'''Pitches enharmonically equal compare unequally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('gf', 4)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert not pitch_1 >= pitch_2
    assert      pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2


def test_NamedPitch___cmp___04():
    r'''Pitches manifestly different compare unequally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('f', 4), pitchtools.NamedPitch('g', 4)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert not pitch_1 >= pitch_2
    assert      pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2


def test_NamedPitch___cmp___05():
    r'''Pitches typographically crossed compare unequally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('fss', 4), pitchtools.NamedPitch('gff', 4)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert not pitch_1 >= pitch_2
    assert      pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2


def test_NamedPitch___cmp___06():
    r'''Pitches test False for equality against unlike instances.
    Other pitch comparisons raise ValueError against unlike instances.'''
    pitch = pitchtools.NamedPitch('c', 4)
    number = 99
    assert not pitch == number
    assert      pitch != number


def test_NamedPitch___cmp___07():
    r'''Pitches with like name, accidental, octave and deviation
        compare equally.'''
    pitch_1 = pitchtools.NamedPitch('bf', 4, -31)
    pitch_2 = pitchtools.NamedPitch('bf', 4, -31)
    assert      pitch_1 == pitch_2
    assert not pitch_1 != pitch_2
    assert not pitch_1 >  pitch_1
    assert      pitch_1 >= pitch_1
    assert not pitch_1 <  pitch_1
    assert      pitch_1 <= pitch_1


def test_NamedPitch___cmp___08():
    r'''Pitches with like name, accidental and ocatve
        but with different deviation compare unequally.'''
    pitch_1 = pitchtools.NamedPitch('bf', 4, 0)
    pitch_2 = pitchtools.NamedPitch('bf', 4, -31)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert      pitch_1 >  pitch_2
    assert      pitch_1 >= pitch_2
    assert not pitch_1 <  pitch_2
    assert not pitch_1 <= pitch_2


def test_NamedPitch___cmp___09():
    r'''Pitches with the same frequency but with different deviation
        do not compare equally.'''
    pitch_1 = pitchtools.NamedPitch('c', 5)
    pitch_2 = pitchtools.NamedPitch('bf', 4, 100)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert      pitch_1 >  pitch_2
    assert      pitch_1 >= pitch_2
    assert not pitch_1 <  pitch_2
    assert not pitch_1 <= pitch_2
