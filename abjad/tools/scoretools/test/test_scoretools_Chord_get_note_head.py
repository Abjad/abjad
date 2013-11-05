# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Chord_get_note_head_01():
    r'''Get note heads by pitch number.
    '''

    chord = Chord("<c' d' b'>4")

    note_head = chord.get_note_head(0)
    assert note_head.written_pitch == 0

    note_head = chord.get_note_head(2)
    assert note_head.written_pitch == 2

    note_head = chord.get_note_head(11)
    assert note_head.written_pitch == 11


def test_scoretools_Chord_get_note_head_02():
    r'''Get note heads by LilyPond input string.
    '''

    chord = Chord("<c' d' b'>4")

    note_head = chord.get_note_head("c'")
    assert note_head.written_pitch == 0

    note_head = chord.get_note_head("d'")
    assert note_head.written_pitch == 2

    note_head = chord.get_note_head("b'")
    assert note_head.written_pitch == 11


def test_scoretools_Chord_get_note_head_03():
    r'''Get note heads by pitch.
    '''

    chord = Chord("<c' d' b'>4")

    pitch = pitchtools.NamedPitch("c'")
    note_head = chord.get_note_head(pitch)
    assert note_head.written_pitch == 0

    pitch = pitchtools.NamedPitch("d'")
    note_head = chord.get_note_head(pitch)
    assert note_head.written_pitch == 2

    pitch = pitchtools.NamedPitch("b'")
    note_head = chord.get_note_head(pitch)
    assert note_head.written_pitch == 11


def test_scoretools_Chord_get_note_head_04():
    '''Raise exceptions when chord has too few or too many note heads.
    '''

    chord = Chord("<c' d' d'>4")

    assert pytest.raises(MissingNoteHeadError, 'chord.get_note_head(9)')
    assert pytest.raises(ExtraNoteHeadError, 'chord.get_note_head(2)')
