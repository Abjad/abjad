# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass___init___01():
    r'''Initializefrom name.
    '''

    assert pitchtools.NamedPitchClass('c') == 'c'
    assert pitchtools.NamedPitchClass('cs') == 'cs'
    assert pitchtools.NamedPitchClass('cf') == 'cf'
    assert pitchtools.NamedPitchClass('cqs') == 'cqs'
    assert pitchtools.NamedPitchClass('cqf') == 'cqf'


def test_pitchtools_NamedPitchClass___init___02():
    r'''Initializefrom other named pitch-class instance.
    '''

    npc = pitchtools.NamedPitchClass('c')
    new = pitchtools.NamedPitchClass(npc)

    assert new == npc
    assert new is not npc


def test_pitchtools_NamedPitchClass___init___03():
    r'''Initializefrom note head instance.
    '''

    chord = Chord([0, 2, 3], (1, 4))
    note_head = chord.note_heads[0]
    npc = pitchtools.NamedPitchClass(note_head)

    assert npc == pitchtools.NamedPitchClass('c')
