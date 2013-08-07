# -*- encoding: utf-8 -*-
from abjad import *


def test_StemTremolo_format_01():
    r'''Tremolo formats correctly on notes.
    '''

    note = Note("cs'4")
    marktools.StemTremolo(8)(note)
    assert note.lilypond_format == "cs'4 :8"
    note.select().detach_marks()
    assert note.lilypond_format == "cs'4"


def test_StemTremolo_format_02():
    r'''Tremolo formats correctly on chords.
    '''

    chord = Chord([1, 2, 3], (1, 4))
    marktools.StemTremolo(8)(chord)
    assert chord.lilypond_format == "<cs' d' ef'>4 :8"
    chord.select().detach_marks()
    assert chord.lilypond_format == "<cs' d' ef'>4"


def test_StemTremolo_format_03():
    r'''Tremolo formats correctly on rests.
    '''

    t = Rest((1, 4))
    marktools.StemTremolo(8)(t)
    assert t.lilypond_format == "r4 :8"
    t.select().detach_marks()
    assert t.lilypond_format == "r4"
