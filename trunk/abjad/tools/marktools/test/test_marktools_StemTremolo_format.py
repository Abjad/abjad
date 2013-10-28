# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_StemTremolo_format_01():
    r'''Tremolo formats correctly on notes.
    '''

    note = Note("cs'4")
    stem_tremolo = marktools.StemTremolo(8)
    attach(stem_tremolo, note)
    assert note.lilypond_format == "cs'4 :8"
    inspect(note).get_mark().detach()
    assert note.lilypond_format == "cs'4"


def test_marktools_StemTremolo_format_02():
    r'''Tremolo formats correctly on chords.
    '''

    chord = Chord([1, 2, 3], (1, 4))
    stem_tremolo = marktools.StemTremolo(8)
    attach(stem_tremolo, chord)
    assert chord.lilypond_format == "<cs' d' ef'>4 :8"
    inspect(chord).get_mark().detach()
    assert chord.lilypond_format == "<cs' d' ef'>4"


def test_marktools_StemTremolo_format_03():
    r'''Tremolo formats correctly on rests.
    '''

    rest = Rest((1, 4))
    stem_tremolo = marktools.StemTremolo(8)
    attach(stem_tremolo, rest)
    assert rest.lilypond_format == "r4 :8"
    inspect(rest).get_mark().detach()
    assert rest.lilypond_format == "r4"
