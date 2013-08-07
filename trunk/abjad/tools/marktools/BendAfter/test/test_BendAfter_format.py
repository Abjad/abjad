# -*- encoding: utf-8 -*-
from abjad import *


def test_BendAfter_format_01():
    r'''Bend formats correctly on notes.
    '''

    note = Note("cs'4")
    marktools.BendAfter(8)(note)
    assert note.lilypond_format == "cs'4 - \\bendAfter #'8.0"
    note.select().detach_marks(marktools.BendAfter)
    assert note.lilypond_format == "cs'4"


def test_BendAfter_format_02():
    r'''Bend formats correctly on chords.
    '''

    chord = Chord([1, 2, 3], (1, 4))
    marktools.BendAfter(8)(chord)
    assert chord.lilypond_format == "<cs' d' ef'>4 - \\bendAfter #'8.0"
    chord.select().detach_marks(marktools.BendAfter)
    assert chord.lilypond_format == "<cs' d' ef'>4"


def test_BendAfter_format_03():
    r'''Bend formats correctly on rests.
    '''

    rest = Rest((1, 4))
    marktools.BendAfter(8)(rest)
    assert rest.lilypond_format == "r4 - \\bendAfter #'8.0"
    rest.select().detach_marks(marktools.BendAfter)
    assert rest.lilypond_format == "r4"
