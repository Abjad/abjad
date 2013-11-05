# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_pitchtools_NamedPitch___cmp___01():
    r'''Referentially equal pitches compare equally.
    '''
    pitch_1 = pitchtools.NamedPitch('fs', 4)
    assert      pitch_1 == pitch_1
    assert not pitch_1 != pitch_1
    assert not pitch_1 >  pitch_1
    assert      pitch_1 >= pitch_1
    assert not pitch_1 <  pitch_1
    assert      pitch_1 <= pitch_1


def test_pitchtools_NamedPitch___cmp___02():
    r'''Pitches equal by name, accidental and octave compare equally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('fs', 4)
    assert      pitch_1 == pitch_2
    assert not pitch_1 != pitch_2
    assert not pitch_1 >  pitch_1
    assert      pitch_1 >= pitch_1
    assert not pitch_1 <  pitch_1
    assert      pitch_1 <= pitch_1


def test_pitchtools_NamedPitch___cmp___03():
    r'''Pitches enharmonically equal compare unequally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('gf', 4)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert not pitch_1 >= pitch_2
    assert      pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2


def test_pitchtools_NamedPitch___cmp___04():
    r'''Pitches manifestly different compare unequally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('f', 4), pitchtools.NamedPitch('g', 4)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert not pitch_1 >= pitch_2
    assert      pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2


def test_pitchtools_NamedPitch___cmp___05():
    r'''Pitches typographically crossed compare unequally.
    '''
    pitch_1, pitch_2 = pitchtools.NamedPitch('fss', 4), pitchtools.NamedPitch('gff', 4)
    assert not pitch_1 == pitch_2
    assert      pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert not pitch_1 >= pitch_2
    assert      pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2


def test_pitchtools_NamedPitch___cmp___06():
    r'''Pitches test False for equality against unlike instances.
    Other pitch comparisons raise ValueError against unlike instances.'''
    pitch = pitchtools.NamedPitch('c', 4)
    number = 99
    assert not pitch == number
    assert      pitch != number
