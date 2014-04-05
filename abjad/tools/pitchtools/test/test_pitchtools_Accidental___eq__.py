# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental___eq___01():
    r'''Accidentals compare equal when they carry the same string.
    '''
    assert pitchtools.Accidental('ff') == pitchtools.Accidental('ff')
    assert pitchtools.Accidental('tqf') == pitchtools.Accidental('tqf')
    assert pitchtools.Accidental('f') == pitchtools.Accidental('f')
    assert pitchtools.Accidental('qf') == pitchtools.Accidental('qf')
    assert pitchtools.Accidental('!') == pitchtools.Accidental('!')
    assert pitchtools.Accidental('qs') == pitchtools.Accidental('qs')
    assert pitchtools.Accidental('s') == pitchtools.Accidental('s')
    assert pitchtools.Accidental('tqs') == pitchtools.Accidental('tqs')
    assert pitchtools.Accidental('ss') == pitchtools.Accidental('ss')


def test_pitchtools_Accidental___eq___02():
    r'''Accidentals compare equal when they carry no string.
    '''
    assert pitchtools.Accidental() == pitchtools.Accidental()
    assert pitchtools.Accidental('') == pitchtools.Accidental('')
    assert pitchtools.Accidental() == pitchtools.Accidental('')


def test_pitchtools_Accidental___eq___03():
    r'''Accidentals compare not equal with only the same adjustment.
    '''
    assert pitchtools.Accidental('') != pitchtools.Accidental('!')


def test_pitchtools_Accidental___eq___04():
    r'''Accidentals do not compare equal to a naked string.
    '''
    assert not pitchtools.Accidental('s') == 's'