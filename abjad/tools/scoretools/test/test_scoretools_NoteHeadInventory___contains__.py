# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadInventory___contains___01():

    chord = Chord("<ef' cs'' f''>4")

    assert 17 in chord.note_heads
    assert 17.0 in chord.note_heads
    assert NamedPitch(17) in chord.note_heads
    assert NamedPitch("f''") in chord.note_heads
    assert chord.note_heads[1] in chord.note_heads
    assert scoretools.NoteHead("f''") in chord.note_heads


def test_scoretools_NoteHeadInventory___contains___02():

    chord = Chord("<ef' cs'' f''>4")

    assert not 18 in chord.note_heads
    assert not 18.0 in chord.note_heads
    assert not NamedPitch(18) in chord.note_heads
    assert not NamedPitch("fs''") in chord.note_heads
    assert not scoretools.NoteHead(18) in chord.note_heads
    assert not scoretools.NoteHead("fs''") in chord.note_heads
