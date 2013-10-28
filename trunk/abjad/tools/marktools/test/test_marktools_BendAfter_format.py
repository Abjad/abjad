# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_BendAfter_format_01():
    r'''Bend formats correctly on notes.
    '''

    note = Note("cs'4")
    bend = marktools.BendAfter(8)
    bend.attach(note)
    assert note.lilypond_format == "cs'4 - \\bendAfter #'8.0"
    inspect(note).get_mark(marktools.BendAfter).detach()
    assert note.lilypond_format == "cs'4"


def test_marktools_BendAfter_format_02():
    r'''Bend formats correctly on chords.
    '''

    chord = Chord([1, 2, 3], (1, 4))
    bend = marktools.BendAfter(8)
    bend.attach(chord)
    assert chord.lilypond_format == "<cs' d' ef'>4 - \\bendAfter #'8.0"
    inspect(chord).get_mark(marktools.BendAfter).detach()
    assert chord.lilypond_format == "<cs' d' ef'>4"


def test_marktools_BendAfter_format_03():
    r'''Bend formats correctly on rests.
    '''

    rest = Rest((1, 4))
    bend = marktools.BendAfter(8)
    bend.attach(rest)
    assert rest.lilypond_format == "r4 - \\bendAfter #'8.0"
    inspect(rest).get_mark(marktools.BendAfter).detach()
    assert rest.lilypond_format == "r4"
