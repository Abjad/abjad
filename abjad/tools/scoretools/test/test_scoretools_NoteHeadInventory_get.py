# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_NoteHeadInventory_get_01():
    r'''Get note heads by pitch number.
    '''

    chord = Chord("<c' d' b'>4")

    note_head = chord.note_heads.get(0)
    assert note_head.written_pitch == 0

    note_head = chord.note_heads.get(2)
    assert note_head.written_pitch == 2

    note_head = chord.note_heads.get(11)
    assert note_head.written_pitch == 11


def test_scoretools_NoteHeadInventory_get_02():
    r'''Get note heads by LilyPond input string.
    '''

    chord = Chord("<c' d' b'>4")

    note_head = chord.note_heads.get("c'")
    assert note_head.written_pitch == 0

    note_head = chord.note_heads.get("d'")
    assert note_head.written_pitch == 2

    note_head = chord.note_heads.get("b'")
    assert note_head.written_pitch == 11


def test_scoretools_NoteHeadInventory_get_03():
    r'''Get note heads by pitch.
    '''

    chord = Chord("<c' d' b'>4")

    pitch = NamedPitch("c'")
    note_head = chord.note_heads.get(pitch)
    assert note_head.written_pitch == 0

    pitch = NamedPitch("d'")
    note_head = chord.note_heads.get(pitch)
    assert note_head.written_pitch == 2

    pitch = NamedPitch("b'")
    note_head = chord.note_heads.get(pitch)
    assert note_head.written_pitch == 11


def test_scoretools_NoteHeadInventory_get_04():
    '''Raise exceptions when chord has too few or too many note heads.
    '''

    chord = Chord("<c' d' d'>4")

    assert pytest.raises(Exception, 'chord.note_heads.get(9)')
    assert pytest.raises(Exception, 'chord.note_heads.get(2)')
