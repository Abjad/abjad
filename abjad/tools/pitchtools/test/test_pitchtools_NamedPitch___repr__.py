# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch___repr___01():
    r'''Named pitch repr is evaluable.
    '''

    named_pitch_1 = NamedPitch("cs''")
    named_pitch_2 = eval(repr(named_pitch_1))

    r'''
    NamedPitch("cs''")
    '''

    assert isinstance(named_pitch_1, NamedPitch)
    assert isinstance(named_pitch_2, NamedPitch)


def test_pitchtools_NamedPitch___repr___02():
    r'''Repr values.
    '''

    named_pitch = NamedPitch("cs''")

    assert repr(named_pitch) == 'NamedPitch("cs\'\'")'
    assert format(named_pitch, 'storage') == 'pitchtools.NamedPitch("cs\'\'")'
